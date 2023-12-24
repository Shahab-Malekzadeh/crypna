from cacheops import invalidate_all
from django.core.cache import caches
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Article, Category
from account.models import User


@receiver(post_delete, sender=User)
def author_post_delete_handler(sender, instance, **kwargs):
    invalidate_all()


@receiver(post_save, sender=User)
def author_post_save_handler(sender, instance, **kwargs):
    invalidate_all()


@receiver(post_delete, sender=Category)
def category_post_delete_handler(sender, instance, **kwargs):
    invalidate_all()


@receiver(post_save, sender=Category)
def category_post_save_handler(sender, instance, **kwargs):
    invalidate_all()


@receiver(post_delete, sender=Article)
def article_post_delete_handler(sender, instance, **kwargs):
    invalidate_all()
    d = caches['detail'].delete(instance.slug)
    print("deleted : ", d)


@receiver(post_save, sender=Article)
def article_post_save_handler(sender, instance, **kwargs):
    invalidate_all()
    caches['detail'].set(instance.slug, instance, timeout=60 * 60 * 24)
    x = caches['detail'].get(instance.slug)
    print(x)
