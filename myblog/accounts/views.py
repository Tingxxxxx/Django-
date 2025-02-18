from django.shortcuts import render,redirect,reverse
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import VerifycodeMode
from django.views.decorators.http import require_http_methods
from .form import *
from django.contrib.auth import get_user_model

import string # 用來取得0~9字串並取樣
import random 

# 初始化用戶實例
User = get_user_model()

# Create your views here.

# 登入
def login(request):
    
    
    return render(request,'login.html')

# 註冊
@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    
    else:
        form = RegisterForm(request.POST)
        # 如果表單驗證成功，將資料存入資料庫(User模型)
        if form.is_valid(): 
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get('password')
            
            # 創建用戶
            User.objects.create_user(username=username,email=email,password=password)

            # 跳轉到登入頁面，讓用戶重新登入
            return redirect(reverse('accounts:login'))
        
        # 表單驗證失敗，則回到註冊頁面
        else:
            print(form.errors)
            # 方式1: 可重渲染註冊模板，且可通過context傳遞的form 來顯示錯誤訊息
            # return render(request,'register.html',context={"form":form}) 
            # 方式2: 重定向跳轉到註冊頁
            return redirect(reverse('accounts:register'))



def send_verify_code(request):
    if request.method == 'GET':
        email = request.GET.get("email")
        if not email:
            return JsonResponse({"code": 400, "message": "缺少 email 參數"})
        
    # 隨機產生四位數驗證碼
    # string.digits="0123456789"
    # random.choices(str,k=) 從str中隨機取k個數(可重複)
    verify_code = "".join(random.choices(string.digits, k=4))
    
    # objects.update_or_create() 用法:
    # 如果資料庫中email已存在，則更新verify_code
    # 如果資料庫中email不存在，則新增該email跟d afaults值
    # 實際業務中驗證碼可存在redis或session中 會比mysql好
    VerifycodeMode.objects.update_or_create(email=email,defaults={'verify_code':verify_code})
    
    # 發送簡單的郵件
    send_mail(
        '驗證信',    # 郵件主題
        f"你的驗證碼為{verify_code}",  # 郵件內容
        None,      # 發送郵件的地址
        [email],    # 收件人的地址
        fail_silently=False,  # 如果發送失敗是否要報錯
    )
    
    return JsonResponse({"code": 200, "message": "驗證信發送成功"}, json_dumps_params={'ensure_ascii': False})

    