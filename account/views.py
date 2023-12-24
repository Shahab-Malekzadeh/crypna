"""
module docstring
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.models import Article

from .forms import ProfileForm, LoginForm
from .mixins import (AuthorAccessMixin, AuthorsAccessMixin, FieldMixin,
                     FormValidMixin, SuperUserAccessMixin)
from .models import User


class ArticleList(AuthorsAccessMixin, ListView):
    """
    class docstring
    """
    template_name = "registration/home.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FormValidMixin, FieldMixin, CreateView):
    """
    class docstring
    """
    model = Article
    template_name = "registration/article-create-update.html"


class ArticleUpdate(AuthorAccessMixin, FormValidMixin, FieldMixin, UpdateView):
    """
    class docstring
    """
    model = Article
    template_name = "registration/article-create-update.html"


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    """
    class docstring
    """
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = "registration/article_confirm_delete.html"


class Profile(LoginRequiredMixin, UpdateView):
    """
    class docstring
    """
    model = User
    template_name = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("account:profile")

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    """
    class docstring
    """
    form_class = LoginForm

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")
