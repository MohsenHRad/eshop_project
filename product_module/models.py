from django.db import models
from django.urls import reverse

from account_module.models import User


# Create your models here.


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return f'{self.title} - {self.url_title}'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=300, verbose_name='عنوان در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        null=True,
        related_name='Products',
        verbose_name='دسته بندی ها'
    )
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند ', null=True, blank=True)
    image = models.ImageField(upload_to="images/products", null=True, blank=True, verbose_name='تصویر محصول')
    price = models.IntegerField(default=0, verbose_name='قیمت')
    short_description = models.CharField(max_length=400, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    product_count = models.IntegerField(verbose_name='تعداد محصول', default=0, null=False, blank=False)

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}  ({self.price})"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    caption = models.CharField(max_length=300)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, related_name='product_tags')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True, verbose_name='کاربر')

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصولات'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product_gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'تصاویر گالری'

