# Django 用戶模型與登入/註冊

## 1. 內建 User 模型

Django 提供了一個內建的 `User` 模型 (`django.contrib.auth.models.User`)，用於管理用戶身份。

### **User 模型的常見欄位**

| 欄位名稱           | 說明       |
| -------------- | -------- |
| `username`     | 用戶名（唯一）  |
| `email`        | 電子郵件（可選） |
| `password`     | 密碼（加密存儲） |
| `is_active`    | 用戶是否啟用   |
| `is_staff`     | 是否是管理員   |
| `is_superuser` | 是否是超級用戶  |
| `date_joined`  | 註冊時間     |

### **如何創建用戶**

```python
from django.contrib.auth.models import User

# 獲取用戶模型，如果未自訂義則返回Django內建的
User = get_user_model() 

# 創建一個用戶（密碼會自動加密存，即資料庫不會顯示明文）
user = User.objects.create_user(username='testuser', email='test@example.com', password='securepassword')
```

**返回值：** `create_user()` 方法會返回新建的 `User` 對象。

---

## 2. `UserCreationForm` 表單類
- Django 內建的 `UserCreationForm` 提供了一個標準的用戶註冊表單。
- 內部會自動執行驗證，並在 form.save() 時將用戶數據存入 Django 內建的 User 模型（或自訂義的 User 模型）。

### **內建驗證**
- `username` 必須唯一，且不能為空、不能包含非法字符。
- `password1`（第一次輸入密碼）和 `password2`（確認密碼）必須匹配。
- `password2` 必須填寫，不可為空。
- 預設要求密碼至少 8 個字符，不能太常見，不能全是數字。

### **使用方式**

```python
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # 綁定用戶提交的數據
        if form.is_valid():
            form.save()  # 表單驗證通過後，儲存用戶到資料庫
            return redirect('login')  # 註冊成功後跳轉到登入頁
    else:
        form = UserCreationForm()  # 如果是 GET 請求，則初始化空白表單
    return render(request, 'register.html', {'form': form})  # 渲染註冊頁面

```

### **自訂用戶創建表單，擴展 `UserCreationForm`**

#### 範例:新增 email 欄位:
```python
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        """ 確保 email 是唯一的 """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("該 email 已被使用")
        return email
```
### **驗證後儲存用戶資料到User模型**
- 調用form.save() 時將用戶數據存入 Django 內建的 User 模型（或自訂義的 User 模型）
- 修改用戶數據前先使用 commit=False
```python
form = UserCreationForm(request.POST)
if form.is_valid():
    user = form.save(commit=False)  # 先不提交到數據庫
    user.email = request.POST.get('email')  # 如果表單中沒有 email 欄位，可以手動添加
    user.save()  # 保存用戶
```

---

## 3. `get_user_model()`

如果自訂了用戶模型（例如擴展 `User` 模型），應該使用 `get_user_model()` 而不是直接引用 `User`。

### **使用方式**

```python
from django.contrib.auth import get_user_model
User = get_user_model()
```

**返回值：** `get_user_model()` 返回當前項目使用的 `User` 模型。

---

## 4. `check_password()`

`check_password()` 用來驗證用戶輸入的密碼是否正確。

### **使用方式**

```python
from django.contrib.auth.models import User

# 獲取用戶對象
user = User.objects.get(username='testuser')

# 驗證密碼
if user.check_password('securepassword'):
    print("密碼正確")
else:
    print("密碼錯誤")
```

**返回值：** `True`（密碼匹配）或 `False`（密碼錯誤）。

---

## 5. `login()`

`login()` 用來讓用戶登入，並將用戶資訊存入 session。可搭配session設置過期時間來實現保持登入功能

### **使用方式**

```python
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.conf import settings
from django.http import HttpRequest
from datetime import timedelta

# 自訂的登錄視圖範例
def user_login(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # 設置 session 過期時間（例如 30 分鐘）
            request.session.set_expiry(timedelta(minutes=30).total_seconds())
            
            # 或使用 settings 設置全局過期時間(預設2周)，如果沒有單獨設置 set_expiry，將使用此配置
            # settings.SESSION_COOKIE_AGE = 1800  # 30 分鐘
            
            return redirect("home")  # 登入成功後跳轉到首頁
        else:
            return render(request, "login.html", {"error": "無效的帳號或密碼"})
    
    return render(request, "login.html")
```

**返回值：** `None`（但會修改 `request` 對象，使用戶保持登入）。

> **注意**：使用 `login()` 之前，必須先通過 `authenticate()` 驗證用戶。

---

## 6. `authenticate()`

`authenticate()` 用於驗證用戶憑據（如用戶名和密碼）。

### **使用方式**

```python
from django.contrib.auth import authenticate

user = authenticate(username='testuser', password='securepassword')
if user is not None:
    print("驗證成功")
else:
    print("驗證失敗")
```

**返回值：** 成功時返回 `User` 對象，失敗時返回 `None`。

### **完整的登入視圖**

```python
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # 登入用戶
            return redirect('home')
        else:
            return render(request, 'login.html', {"error": "帳號或密碼錯誤"})
    return render(request, 'login.html')
```

---

## 🔥 **總結**

| 方法                           | 作用                   | 返回值 |
| ---------------------------- | -------------------- | ----- |
| `User.objects.create_user()` | 創建用戶並加密密碼            | `User` 對象 |
| `UserCreationForm`           | 內建的用戶註冊表單，含基礎驗證      | `is_valid()` 返回 `True` 或 `False`， `save()` 返回 `User` |
| `get_user_model()`           | 獲取當前使用的用戶模型（適用於自訂模型） | `User` 類 |
| `check_password()`           | 檢查密碼是否正確             | `True` 或 `False` |
| `authenticate()`             | 驗證用戶憑據（帳號+密碼）        | `User` 或 `None` |
| `login()`                    | 讓用戶登入並存入 session     | `None` |

