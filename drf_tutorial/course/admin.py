from django.contrib import admin
from .models import Course
# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'introduction', 'teacher', 'price'] # 顯示的欄位
    search_fields = list_display # 可在後台搜索的欄位
    list_filter = list_display # 可在後台使用下拉篩選的欄位


