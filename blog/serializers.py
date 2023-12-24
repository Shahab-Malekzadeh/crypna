from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField()
    jpublish = serializers.CharField()
    category_to_str = serializers.CharField()
    when_published = serializers.CharField()
    publish = serializers. DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Article
        fields = ['id', 'author_name', 'title', 'slug', 'editors_choice', 'description', 'thumbnail',
                  'publish', 'jpublish', 'category_to_str', 'when_published', ]
