from django.db import models


# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, verbose_name='آدرس')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='فکس')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل')
    copy_right = models.TextField(verbose_name='متن کپی رایت سایت')
    about_us_text = models.TextField(verbose_name='متن درباره ما سایت')
    site_logo = models.ImageField(upload_to='images/site-setting/', verbose_name='لوگو سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    is_active = models.BooleanField(verbose_name='فعال')

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLinks(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=700, verbose_name='آدرس url')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, verbose_name='دسته بندی', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='آدرس لینک')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    description = models.TextField(max_length=700, verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/slider', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(verbose_name='فعال', default=False)

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'

    def __str__(self):
        return self.title


# site_banner_choices = [  ==> لیست دارپ دون و گزینه های پوزیشن بنر سایت
#     ('product_list', 'صفحه لیست محصولات'),
#     ('product_detail', 'صفحه جزئیات محصولات')
# ]


class SiteBanner(models.Model):
    class BannerPositionChoices(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات',
        product_detail = 'product_detail', 'صفحه جزئیات محصولات',
        about_us = 'about_us', 'صفحه درباره ما',

    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url_title = models.URLField(max_length=500, null=True, blank=True, verbose_name='آدرس بنر')
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    position = models.CharField(max_length=200, choices=BannerPositionChoices.choices, verbose_name='جایگاه نمایشی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنر های تبلیغاتی'
