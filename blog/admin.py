"""
module docstring
"""

from django.contrib import admin

from .models import Article, Category, IPAddress

# Admin header change
admin.site.site_header = "Django Admin Panel"


def make_published(modeladmin, request, queryset):
    """
    function docstring
    """
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "published."
    else:
        message_bit = "published."
    modeladmin.message_user(request, "{} articles {}".format(rows_updated, message_bit))


make_published.short_description = "Publish Selected Articles."


def make_draft(modeladmin, request, queryset):
    """
    function docstring
    """
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        message_bit = "Drafted."
    else:
        message_bit = "Drafted."
    modeladmin.message_user(request, "{} articles {}".format(rows_updated, message_bit))


make_draft.short_description = "Draft Selected Articles."


class CategoryAdmin(admin.ModelAdmin):
    """
    class docstring
    """
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    """
    class docstring
    """
    list_display = ('title', 'thumbnail_tag', 'slug', 'author',
                    'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['status', '-publish']
    actions = [make_published, make_draft]

    class Media:
        css = {
            "all": ("registration/admin-panel/assets/css/tiny_mce.css",)
        }
        js = ("registration/admin-panel/assets/js/tiny_mce.js",)


admin.site.register(Article, ArticleAdmin)

admin.site.register(IPAddress)
