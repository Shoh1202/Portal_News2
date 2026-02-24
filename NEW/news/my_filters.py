from django_filters import FilterSet
from django import forms
from .models import Post
class PostFilter(FilterSet):
   class Meta:
       model=Post
       fields={'title':['icontains'],
           'author':['exact'],
               'time_add':['gt']}
