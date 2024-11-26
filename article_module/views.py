from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView

from article_module.models import Article, ArticleCategory, ArticleComment


# class ArticlesView(View):
#     def get(self, request):
#         articles = Article.objects.filter(is_active=True).first()
#         context = {'articles': articles}
#
#         return render(request, 'article_module/articles_page.html', context)


# Create your views here.

class ArticlesListView(ListView):
    model = Article
    paginate_by = 5
    template_name = 'article_module/articles_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticlesListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_category__url_title__iexact=category_name)

        query = query.filter(is_active=True)
        return query


def article_categories_component(request: HttpRequest):
    article_main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,
                                                                                                     parent_id=None)
    context = {
        'main_categories': article_main_categories
    }
    return render(request, 'article_module/components/article_categories_component.html', context)


class ArticlesDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_queryset(self):
        query = super(ArticlesDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticlesDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, is_accepted=True,
                                                            parent=None).order_by('-create_date').prefetch_related(
            'articlecomment_set')
        return context


def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        print(article_id, article_comment, parent_id)
        new_comment = ArticleComment(article_id=article_id, text=article_comment, user_id=request.user.id,
                                     is_accepted=True, parent_id=parent_id)
        new_comment.save()
        context = {
            'comments': ArticleComment.objects.filter(article_id=article_id, is_accepted=True,
                                                      parent=None).order_by('-create_date').prefetch_related(),
            'comments_count': ArticleComment.objects.filter(article_id=article_id).count()
        }
        return render(request, 'article_module/includes/article_comment_partial.html', context)
    return HttpResponse('Response')
