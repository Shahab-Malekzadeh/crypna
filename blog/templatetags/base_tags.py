from django import template
from ..models import Category, Article
from account.models import User

register = template.Library()


@register.inclusion_tag("blog/partials/category_navbar.html")
def categories():
    return {
        "all_categories": Category.objects.active(),
    }


@register.inclusion_tag("blog/partials/author_navbar.html")
def authors():
    return {
        "all_authors": User.objects.filter(is_author=True),
    }


@register.inclusion_tag("blog/partials/article_sidebar.html")
def articles():
    return {
        "all_articles": Article.objects.published()[:3],
    }
