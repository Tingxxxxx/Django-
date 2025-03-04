from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# 課程信息模型類
class Course(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text='課程名稱', verbose_name='課程名稱')
    introduction = models.TextField(help_text='課程介紹', verbose_name='課程介紹')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, help_text='講師', verbose_name='講師')
    price = models.DecimalField(max_digits=6,decimal_places=2, help_text='價格', verbose_name='課程價格')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間') 

    class Meta:
        verbose_name = '課程訊息'
        verbose_name_plural = '課程訊息'
        ordering = ['price']

    def __str__(self):
        return self.name
