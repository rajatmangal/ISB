import django_filters
from django_filters import CharFilter
# from django_filters import
from .models import *


class PostFilter(django_filters.FilterSet):
    text = CharFilter(field_name="text", lookup_expr='icontains')
    description = CharFilter(field_name="description", lookup_expr='icontains')
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['date_created', 'userid']
