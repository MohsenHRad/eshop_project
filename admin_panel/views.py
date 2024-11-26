from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView

from article_module.models import Article


def permission_checker_decorator_factory(data=None):
    def permission_checker_decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            print(data)
            if request.user.is_authenticated and request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse('login_page'))

        return wrapper

    return permission_checker_decorator


@permission_checker_decorator_factory({'permission_name': 'admin_index'})
def index(request: HttpRequest):
    return render(request, 'admin_panel/home/index.html')
    # if request.user.is_authenticated:
    #     if request.user.is_superuser:
    # return redirect(reverse('login_page'))


@method_decorator(permission_checker_decorator_factory({'permission_name': 'articles_list'}), name='dispatch')
class ArticlesListView(ListView):
    model = Article
    paginate_by = 12
    template_name = 'admin_panel/_admin_articles/articles_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticlesListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_category__url_title__iexact=category_name)
        return query


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class ArticleEditView(UpdateView):
    model = Article
    template_name = 'admin_panel/_admin_articles/edit_article.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_articles')
    # success_url = '/admin-panel/_admin_articles/'
