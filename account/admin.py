"""
module docstring
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

UserAdmin.fieldsets[2][1]['fields'] = (
    'bio',
    'is_active',
    'is_staff',
    'is_superuser',
    'is_author',
    'groups',
    'user_permissions',
)
UserAdmin.list_display += ('is_author',)

admin.site.register(User, UserAdmin)
