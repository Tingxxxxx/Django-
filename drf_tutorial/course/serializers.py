from .models import Course
from django.contrib.auth.models import User
from rest_framework import serializers

# 課程訊息的序列化器
class CourseSerializer(serializers.ModelSerializer):
    # 複寫 課程模型中的 teacher 欄位，指定source參數來獲取老師名，並設為只讀
    teacher = serializers.CharField(source='teacher.username', read_only=True)  # teacher外鍵關聯到User模型，並通過.username獲取值
    
    class Meta:
        model = Course
        fields = "__all__"  # 更正為__all__

# 用戶模型的序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
