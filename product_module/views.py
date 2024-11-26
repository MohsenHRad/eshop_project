from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from site_module.models import SiteBanner
from utils.convertors import group_list
from utils.http_service import get_client_ip
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery


# Create your views here.
class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['price']
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        # db_min_price = query.order_by('price').first().price
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0

        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.BannerPositionChoices.product_list)

        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query

    # def get_queryset(self):
    #     base_query = super(ProductListView, self).get_queryset()
    #     data = base_query.filter(is_active=True)
    #     return data


# class ProductListView(TemplateView):
#     template_name = 'product_module/product_list.html'

# def get_context_data(self, **kwargs):
#     product = Product.objects.all().order_by('-price')[:5]
#     context = super(ProductListView, self).get_context_data()
#     context['products'] = product
#     return context


# def product_list(request):
#     product = Product.objects.all().order_by('-price')
#     # number_of_product = product.count()
#     # avg_rating = product.aggregate(Avg("rating"), Min("price"))
#     return render(request, 'product_module/product_list.html', {
#         "products": product,
#         # "total_number_of_products": number_of_product,
#         # "average_rating": avg_rating
#     })


# def get_context_data(self, **kwargs):
#     context = super(ProductDetailView, self).get_context_data()
#     slug = kwargs['slug']
#     product = get_object_or_404(Product, slug=slug)
#     context['products'] = product
#     return context


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    context_object_name = 'product'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get("product_favorites")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.BannerPositionChoices.product_detail)
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_galleries_group'] = group_list(galleries, 3)
        context['related_product'] = group_list(
            list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12]), 3)
        # request.user.id
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context


# def product_detail(request, slug):
#     # try:
#     #     return render(request, 'product_module/product_detail.html', {
#     #         "products": Product.objects.get(id=product_id)})
#     # except:
#     #     raise Http404
#     product = get_object_or_404(Product, slug=slug)
#
#     return render(request, 'product_module/product_detail.html', {
#         "products": product
#     })


class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product_favorites"] = product.id
        # return redirect(reversed(product_id))
        return redirect(product.get_absolute_url())


def product_categories_component(request: HttpRequest):
    Product_Categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': Product_Categories
    }
    return render(request, 'product_module/component/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/component/product_brands_component.html', context)

# my_list = range(1, 13)
# res_list = [[1, 2, 3, 4], [5, 6, 7, 8, ], [9, 10, 11, 12]]
# final_list = []
# group_size = 3
# my_range = range(0, len(my_list), group_size)
# print(list(my_range))
#
# for i in my_range:
#     final_list.append(list(my_list[i:i + group_size]))
#
# print(final_list)
