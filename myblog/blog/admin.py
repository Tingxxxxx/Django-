from django.contrib import admin
from .models import *
# Register your models here.

# 自訂義admin系統顯示的模型類
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'pub_time', 'author', 'category' ]

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'blog', 'content', 'pub_time']