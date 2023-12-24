"""
module docstring
"""

import math

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.text import slugify

from account.models import User
from extensions.utils import jalali_converter


# Managers
class ArticleManager(models.Manager):
    """
    class docstring
    """
    def published(self):
        return self.filter(status='p')


# Managers
class CategoryManager(models.Manager):
    """
    class docstring
    """
    def active(self):
        return self.filter(status=True)


class IPAddress(models.Model):
    """
    class docstring
    """
    ip_address = models.GenericIPAddressField(verbose_name='ip address')


class Category(models.Model):
    """
    class docstring
    """
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='children',
                               verbose_name='Sub Category')
    title = models.CharField(max_length=200, verbose_name="Category Title")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Category Slug")
    status = models.BooleanField(default=True, verbose_name="show?")
    position = models.IntegerField(verbose_name="Position in the list")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['parent__id', 'position']

    def __str__(self):
        return str(self.title)

    objects = CategoryManager()


class Article(models.Model):
    """
    class docstring
    """
    STATUS_CHOICES = (
        ('d', 'Draft'),  # draft
        ('p', 'Published'),  # published
        ('i', 'Pending'),  # investigation
        ('b', 'Backed'),  # back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               related_name='auth_art', verbose_name="Author")
    title = models.CharField(max_length=200, verbose_name="Article Title")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Article slug")
    category = models.ManyToManyField(Category, verbose_name="Category", related_name="cat_art")
    editors_choice = models.BooleanField(default=False, verbose_name="Editor's Choice")
    description = models.TextField(verbose_name="Description")
    thumbnail = models.ImageField(upload_to='image/', verbose_name="Thumbnail")
    publish = models.DateTimeField(default=timezone.now, verbose_name="Publish time")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="Status")
    admin_comment = models.TextField(blank=True, null=True, verbose_name="Admin & Author discussion")
    hits = models.ManyToManyField(IPAddress, blank=True, related_name='hits', verbose_name='Visits')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug, allow_unicode=True)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-publish"]

    def get_absolute_url(self):
        return reverse("account:home")

    def author_name(self):
        if self.author.get_full_name():
            return self.author.get_full_name()
        else:
            return self.author.username

    def jpublish(self):
        return jalali_converter(self.publish)

    jpublish.short_description = "Publish time"

    def thumbnail_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'"
                           .format(self.thumbnail.url))

    thumbnail_tag.short_description = "Thumbnail"

    def category_to_str(self):
        return "، ".join([category.title for category in self.category.active()])

    category_to_str.short_description = "Category"

    def when_published(self):
        """
        function docstring
        """
        now = timezone.now()

        diff = now - self.publish

        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + " second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if 1 <= diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if 30 <= diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    objects = ArticleManager()


from .signals import *
