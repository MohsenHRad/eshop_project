from django.contrib import admin

from . import models


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_filter = ['price', 'category']
    list_display = ['title', 'price', 'is_active', 'product_count']
    list_editable = ['price', 'is_active', 'product_count']


class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['image', 'product']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery, ProductGalleryAdmin)
