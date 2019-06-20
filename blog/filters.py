from .models import Post
import django_filters


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['title', 'category', 'author', ]