from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic.base import TemplateView

from product_module.models import Product, ProductCategory
from site_module.models import SiteSetting, FooterLinkBox, Slider
from utils.convertors import group_list


# Create your views here.
# def index_page(request):
#     return render(request, 'home_module/index_page.html')

# class HomeView(View):
#     def get(self, request):
#         context = {
#             'data': 'this is data'
#         }
#         return render(request, 'home_module/index_page.html', context)


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        # return super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        # context['data'] = 'this is date in home page'
        # context['message'] = 'this is message in home page'
        context['slider'] = Slider.objects.filter(is_active=True)
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        context['latest_products'] = group_list(latest_products, 2)
        most_visited_product = Product.objects.filter(is_delete=False, is_active=True).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        # print(group_list(latest_products, 2))
        context['most_visited_product'] = group_list(most_visited_product, 4)
        categories = list(
            ProductCategory.objects.annotate(product_count=Count('Products')).filter(is_active=True,
                                                                                     is_delete=False,
                                                                                     product_count__gt=0)[:6])
        categories_product = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.Products.all()[:4])

            }
            categories_product.append(item)
        context['categories_products'] = categories_product
        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:12]

        context['most_bought_product'] = group_list(most_bought_products)

        return context


def contact_page(request):
    return render(request, 'home_module/contact_page.html')


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    for item in footer_link_boxes:
        item.footerlinks_set

    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context
