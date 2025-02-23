from .models import *
from django import forms
# 發布文章的模型表單驗證

class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=200, min_length=2)
    content = forms.CharField(min_length=2)
    category = forms.IntegerField()


class PubCommentForm(forms.Form):
    content = forms.CharField(required=True,max_length=200)
    blog_id = forms.IntegerField()
    
    