import datetime
import json
import time

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from product_module.models import Product
from .models import Order, OrderDetail

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/order/verify-payment/'


def add_product_to_order(request: HttpRequest):
    # print(request.GET)
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        # count = 1
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نمی باشد',
            'icon': 'error',
            'confirm_button_text': 'مرسی از شما'
        })

    # print(f'productid is : {product_id} and product count is : {count}')

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            # current_order = Order.objects.filter(is_paid=False, user_id=request.user.id).first()
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_order_deail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_order_deail.save()

            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
                'icon': 'success',
                'confirm_button_text': 'باشه، ممنونم'
            })
        else:
            return JsonResponse({
                'status': 'Not Found',
                'text': 'محصول مورد نظر یافت نشد',
                'icon': 'error',
                'confirm_button_text': 'باشه، ممنونم'
            })
    else:
        return JsonResponse({
            'status': 'Not_Authenticated',
            'text': 'برای افزودن محصول به سبد خرید میبایست ابتدا وارد سایت شوید',
            'icon': 'info',
            'confirm_button_text': 'ورود به سایت',
        })


@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    print(request.user)
    print(request.user.id)
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price,
        "Authority": request.GET("Authority"),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            current_order.is_paid = True
            current_order.payment_date = time.time()
            current_order.save()
            # return {'status': True, 'RefID': response['RefID']}
            ref_str = response = response.json()['data']['refId']
            return render(request, 'order_module/payment_result.html', {
                'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
            })
        else:
            ref_str = response = response.json()['data']['refId']
            return render(request, 'order_module/payment_result.html', {
                'info': f'تراکنش مورد نظر با کد پیگیری{ref_str} با موفقیت انجام نشد'
            })
    return response
