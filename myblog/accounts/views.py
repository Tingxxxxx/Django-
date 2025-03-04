from django.shortcuts import render,redirect,reverse
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from .models import VerifycodeMode
from django.views.decorators.http import require_http_methods
from .form import *
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib import messages
import string # 用來取得0~9字串並取樣
import random 

# 初始化用戶實例
User = get_user_model()

# Create your views here.

# 登入
@require_http_methods(['GET', 'POST'])  
def user_login(request):
    if request.method == 'POST':  
        form = LoginForm(request.POST)
        if form.is_valid():  # 表單數據驗證
            email = form.cleaned_data.get('email')  
            password = form.cleaned_data.get('password')  
            remember = form.cleaned_data.get('remember') 

            # 根據用戶輸入的信箱到資料庫查詢是否有對應的用戶資料
            user = User.objects.filter(email=email).first()  # first()：有查到會返回 user 對象，沒查到返回 None

            # 如果該用戶存在，且密碼正確
            if user and user.check_password(password):
                # 使用 login 函數登入，且該函數會自動將資料存到 session
                login(request, user)

                # 如果用戶未勾選記住我
                if not remember:
                    # 0 表示瀏覽器關閉就清除 session 資料
                    request.session.set_expiry(0)
                    # 用戶有勾選記住我則使用 Django 默認設置（兩周）

                return redirect('/')  # 登入成功後跳轉到首頁
            else:
                # 用戶登入失敗，顯示錯誤訊息
                messages.error(request, '信箱或密碼錯誤')  # 顯示錯誤訊息
                print('信箱或密碼錯誤') # 僅後端開發測試用，實際業務開發可用ajax+js前端再處理
    else:  # 處理 GET 請求
        form = LoginForm()  # 初始化空白表單

    return render(request, 'login.html', {'form': form})  # 渲染登錄頁面

# 登出
def user_logout(request):
    # 使用logout()函數 會自動刪除session
    logout(request) 
    return redirect('/')

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
            messages.error(request, '註冊失敗,請重新註冊')  # 顯示錯誤訊息
            # 方式1: 可重渲染註冊模板，且可通過context傳遞的form 來顯示錯誤訊息
            return render(request,'register.html',context={"form":form}) 
            # 方式2: 重定向跳轉到註冊頁
            # return redirect(reverse('accounts:register'))



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
