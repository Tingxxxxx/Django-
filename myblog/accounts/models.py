from django.db import models


# Create your models here.

# 驗證碼模型
class VerifycodeMode(models.Model):
    email = models.EmailField(unique=True) # 信箱必須唯一
    verify_code = models.CharField(max_length=4)
    create_at = models.DateTimeField(auto_now_add=True) # 創建時間
