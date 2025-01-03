from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView

from account_module.models import User
from order_module.models import Order, OrderDetail
from .forms import EditProfileModelForm, ChangePasswordForm


@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


def user_panel_menu_component(request: HttpRequest):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html')


@method_decorator(login_required, name='dispatch')
class EditUserProfile(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        #     initial={
        #     'first_name': current_user.first_name,
        #     'last_name': current_user.last_name,
        #     'avatar': current_user.avatar,
        #     'address': current_user.address,
        # })
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordPage(View):
    def get(self, request: HttpRequest):
        context = {
            'form': ChangePasswordForm()
        }
        return render(request, 'user_panel_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user is not None and current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('password', 'کلمه عبور وارد شده اشتباه می باشد')

        context = {
            'form': form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)


@method_decorator(login_required, name='dispatch')
class UserShopping(ListView):
    model = Order
    template_name = 'user_panel_module/user_shopping.html'
    context_object_name = 'order_detail_set'

    def get_queryset(self):
        queryset = super().get_queryset()
        request: HttpRequest = self.request
        queryset = queryset.filter(user_id=request.user.id, is_paid=True)

        return queryset


@login_required
def user_panel_menu_component(request: HttpRequest):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html')


# @login_required(login_url='login_page')
@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)

    total_amount = current_order.calculate_total_price()
    context = {
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'user_panel_module/user_basket.html', context)


@login_required
def remove_order_detail(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'Not Found detail_id'
        })
    # current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
    #
    #                                                                                          user_id=request.user.id)
    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                             order__user_id=request.user.id).delete()
    # detail = current_order.orderdetail_set.filter(id=detail_id).first()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'Detail Not Found'
        })
    # detail.delete()

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    data = render_to_string('user_panel_module/user_basket_content.html', context)
    return JsonResponse({
        'status': 'Success',
        'body': data
    })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'detail_id or state Not Found '
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'order detail not found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'invalid State'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    data = render_to_string('user_panel_module/user_basket_content.html', context)
    return JsonResponse({
        'status': 'Success',
        'body': data
    })


def user_shopping_detail(request: HttpRequest, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=request.user.id).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')

    return render(request, 'user_panel_module/user_shopping_detail.html', {
        'order': order
    })
