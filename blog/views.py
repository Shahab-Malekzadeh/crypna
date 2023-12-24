"""
module docstring
"""
import json
from datetime import datetime, timedelta

from django.core.cache import caches
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from account.mixins import AuthorAccessMixin
from account.models import User

from .models import Article, Category
from .serializers import ArticleSerializer

global last_week
last_week = datetime.now() - timedelta(days=7)


# Index page (first page of the site)
def home(request):
    """
    function docstring
    """
    all_articles = Article.objects.prefetch_related(
        "author",
    ).filter(status='p', publish__gte=last_week).defer(
        "description", "admin_comment", "hits",
    )

    editors_choice = Article.objects.prefetch_related(
        "author",
    ).filter(status='p', editors_choice=True)[:5].defer(
        "description", "admin_comment", "hits",
    )

    hot_news = Article.objects.prefetch_related(
        "hits"
    ).filter(publish__gte=last_week).annotate(
        count=Count('hits')
    ).order_by('-count', '-publish')[:5].defer(
        "description", "admin_comment", "hits",
    )

    post_grid = Article.objects.prefetch_related(
        "author",
    ).filter(status='p', publish__gte=last_week)[:3].defer(
        "admin_comment", "hits",
    )

    context = {
        "all_articles": all_articles,
        "editors_choice": editors_choice,
        "hot_news": hot_news,
        "post_grid": post_grid,
    }
    return render(request, 'blog/home.html', context)


# Add authentication_classes & permission_classes to show more posts to everyone!
@api_view()
@authentication_classes([SessionAuthentication])
@permission_classes((AllowAny,))
def load_more(request):
    """
    function docstring
    """
    card_count = request.GET.get("card_count")
    print(card_count)
    no_more_article = False

    article_count = Article.objects.filter(status='p').values('id', ).count()

    try:
        if article_count <= int(card_count) + 3:
            no_more_article = True
            articles = Article.objects.select_related("author").filter(status='p').defer(
                'admin_comment', 'hits',
            )
        else:
            articles = Article.objects.select_related("author").filter(status='p').defer(
                'admin_comment', 'hits',
            ).order_by('-publish')[:int(card_count) + 3]

    except Article.DoesNotExist:
        raise Article.DoesNotExist('No Articles')

    serializer = ArticleSerializer(articles, many=True)

    data = {
        "no_more_article": no_more_article,
        "serialized_obj": serializer.data,
    }
    return Response(json.dumps(data))


class ArticleList(ListView):
    """
    class docstring
    """
    queryset = Article.objects.prefetch_related(
        "author", "category", "hits"
    ).filter(status='p', publish__gte=last_week)


class MyDetailView(DetailView):
    """
    class docstring
    """
    model = Article
    template_name = 'blog/article_detail.html'


class ArticleDetail(MyDetailView):
    """
    class docstring
    """

    def get_object(self, **kwargs):
        slug = self.kwargs.get('slug')
        obj = caches['detail'].get(slug)

        if obj:
            article = obj
        else:
            article = get_object_or_404(
                Article.objects.prefetch_related("author", "category", "hits").filter(status='p'),
                slug=slug
            )

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article


class ArticlePreview(AuthorAccessMixin, DetailView):
    """
    class docstring
    """

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


global category


class CategoryList(ListView):
    """
    class docstring
    """
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.cat_art.select_related("author").filter(status='p')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    """
    class docstring
    """
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.auth_art.prefetch_related("category").filter(status='p')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
