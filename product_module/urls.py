from django.urls import path

from . import views

urlpatterns = [
    # path('', views.product_list, name='product_list'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_categories_list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product_brands_list'),
    # path('<slug:slug>', views.product_detail, name='product-detail')
    path('product-favorite', views.AddProductFavorite.as_view(), name='product-favorite'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail')

]
