from django import forms
from django.contrib.auth import get_user_model  # 導入自訂的用戶模型(如沒重寫，則會導入django預設的)
from .models import VerifycodeMode
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# 初始化用戶實例
User = get_user_model()

# 定義註冊驗證表單
class RegisterForm(forms.Form):
    username = forms.CharField(
    max_length=20,
    min_length=3,
    error_messages={
        'required': '請輸入用戶名',
        'max_length': '用戶名不能超過20個字符',
        'min_length': '用戶名不能少於3個字符'
        }
    )
    email = forms.EmailField(error_messages={
        'required':'請輸入電子信箱',
        'invalid':'請輸入正確的電子信箱'
    })

    verifycode = forms.CharField(max_length=4,error_messages={
        'required':'請輸入驗證碼'
    })

    password = forms.CharField(
        max_length=20,
        min_length=6,
        error_messages={
            'required': '請輸入密碼',
            'max_length': '密碼不能超過20個字符',
            'min_length': '密碼不能少於6個字符'
        }
    )

    # 重寫驗證方法
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # 檢查 email 是否為 None
        if not email:
            raise forms.ValidationError('請輸入電子信箱')        

        # 檢查信箱是否已被註冊過了
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('該信箱已被註冊')
        # 如驗證成功，返回email
        return email

    
    def clean_verifycode(self):
        # 獲取用戶輸入的驗證碼、信箱
        verify_code = self.cleaned_data.get('verifycode')
        email = self.cleaned_data.get('email')

        # 先確保信箱已通過驗證且存在
        if not email:
            raise forms.ValidationError('請先輸入電子信箱')

        # .first()方法，如果存在會返回第一條數據，如果不存在則返回None
        verifycodemodel = VerifycodeMode.objects.filter(email=email,verify_code=verify_code).first()
        # 如果該模型不存在，代表驗證碼與信箱不匹配
        if not verifycodemodel:
            raise forms.ValidationError('驗證碼錯誤') 
        # 如果沒有拋出異常，代表驗證成功，則刪除已使用的驗證碼
        verifycodemodel.delete()
        return verify_code



        
class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={
        "required":'請輸入電子信箱',
        'invalid':'請輸入有效的電子信箱'})
    password = forms.CharField(max_length=20,min_length=6,error_messages={
        'max_length':'秘密必須在6~20位之間',
        'min_length':'秘密必須在6~20間'})
    remember = forms.IntegerField(required=False)  # 記住我，可允許留空
