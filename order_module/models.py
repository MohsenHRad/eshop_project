from django.db import models

from account_module.models import User
from product_module.models import Product


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='نهایی شده/نشده')
    payment_date = models.DateTimeField(null=True, editable=True, blank=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return str(self.user)

    # def convert_date_stamp(self):
    #     date_time = 0
    #     # if self.is_paid:
    #
    #     # for date in self.orderdetail_set.all():
    #     #     date_time += datetime.combine(self.payment_date, datetime.min.time())
    #     #     print(self.payment_date)
    #     #     payment_datetime = datetime.combine(self.payment_date, datetime.min.time())
    #     #     return payment_datetime
    #     # else:
    #     #     return None

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.product.price * order_detail.count

        return total_amount


class Meta:
    verbose_name = 'سبد خرید'
    verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='نام محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        return self.count * self.product.price

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'
