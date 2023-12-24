"""
module docstring
"""

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from blog.models import Article


class FieldMixin:
    """
    class docstring
    """
    def dispatch(self, request, *args, **kwargs):
        self.fields = [
            "title", "slug", "category", "editors_choice", "description",
            "thumbnail", "publish", "status", "admin_comment"
        ]
        if request.user.is_superuser:
            self.fields.append("author")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    """
    class docstring
    """
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status in ['d', 'i']:
                self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin:
    """
    class docstring
    """
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.status in ['b', 'd'] or \
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("<h1>You can't see this page!</h1>")


class AuthorsAccessMixin:
    """
    class docstring
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect("login")


class SuperUserAccessMixin:
    """
    class docstring
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("<h1>You can't see this page!</h1>")
