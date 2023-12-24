"""
module docstring
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    class docstring
    """

    email = models.EmailField(unique=True, verbose_name='Email')
    is_author = models.BooleanField(default=False, verbose_name='is author')
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
