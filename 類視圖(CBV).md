# Django 類視圖（Class-Based Views, CBV）

## 1. 什麼是類視圖？

Django 提供了基於類的視圖（CBV），用來替代傳統的基於函數的視圖（FBV）。
類視圖的優勢包括：
- **重用性**：允許透過繼承與 Mixin 組合來重用代碼。
- **可讀性**：將不同的 HTTP 方法（如 GET、POST）拆分到不同的類方法中。
- **擴展性**：可利用 Django 內建的通用視圖，減少重複工作。

---

## 2. CBV 的基本使用

### 2.1 繼承 `View` 類

Django 提供了 `View` 類作為所有 CBV 的基礎。

#### 範例:
```python
from django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request):
        return HttpResponse('這是 GET 請求')
    
    def post(self, request):
        return HttpResponse('這是 POST 請求')

✅如果類視圖中沒有定義相關http請求方法(如 PUT、DELETE、PATCH 方法)，瀏覽器卻發送該請求，則會產生`405Method Not Allowed`異常
```

在 `urls.py` 中註冊視圖時，需要使用 `.as_view()` 方法：

```python
from django.urls import path
from .views import MyView

urlpatterns = [
    path('my-view/', MyView.as_view(), name='my_view'),
]
```

### 2.2 `as_view()` 解析
用於將類視圖轉換為可以處理請求的函數視圖。使類視圖就可以像函數視圖一樣在 URL 配置中使用。

**工作原理:**
- as_view() 方法創建了一個視圖實例，並返回一個可以處理請求的可調用對象。
- 當客戶端發送請求時，這個可調用對象會調用相應的 HTTP 方法（例如 get、post 等）來處理請求。


---

## 3. 通用類視圖（Generic Views）

Django 提供了一些內建的通用類視圖來處理常見的 CRUD 操作。

---
### 3.1 `TemplateView` - 渲染靜態頁面

#### 範例:
```python
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
```
---
### 3.2 `ListView` - 列表視圖

用於顯示多個對象的列表的通用視圖。它自動提供了處理和顯示對象列表的功能。
- 自動查詢所有對象
- 自動傳遞上下文數據context
- 靈活的過濾和排序(覆寫 `get_queryset`)
- 內建分頁功能(`paginate_by`)

#### 範例:
```python
from django.views.generic import ListView
from .models import Article

class ArticleListView(ListView):
    model = Article # ListView 會自動查詢所有 Article 對象
    template_name = 'article_list.html'
    context_object_name = 'articles'  # 在模板中使用的上下文變量名稱
    paginate_by = 10  # 每頁顯示10篇文章

    #　覆寫 get_queryset 方法來實現更複雜的查詢邏輯。
    def get_queryset(self): 
        return Article.objects.filter(published=True).order_by('-created_at')
```

**模板範例:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Article List</title>
</head>
<body>
    <h1>文章列表</h1>
    <ul>
        {% for article in articles %}
            <li>{{ article.title }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

**URL 配置:**
```python
from django.urls import path
from .views import ArticleListView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
]
```
---
### 3.3 `DetailView` - 詳細視圖

用於顯示單個對象的詳細資訊。

#### 範例:

```python
from django.views.generic import DetailView
from .models import Article

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
```

**模板範例:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Article Detail</title>
</head>
<body>
    <h1>{{ article.title }}</h1>
    <p>{{ article.content }}</p>
</body>
</html>
```

**URL 配置:**
```python
from django.urls import path
from .views import ArticleDetailView

urlpatterns = [
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
]
```
---
### 3.4 `CreateView` - 創建視圖

用於新增資料。

#### 範例:
```python
from django.views.generic import CreateView
from .models import Article
from django.urls import reverse_lazy

class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'article_form.html'
    success_url = reverse_lazy('article_list')  # 創建成功後的重定向網址
```

**URL 配置:**
```python
from django.urls import path
from .views import ArticleCreateView

urlpatterns = [
    path('article/new/', ArticleCreateView.as_view(), name='article_create'),
]
```
---
### 3.5 `UpdateView` - 更新視圖

用於更新現有的模型實例。這個視圖將自動提供一個表單，允許用戶更新指定的字段，並在成功後重定向到一個指定的 URL。

#### 範例:
**用戶訪問 http://127.0.0.1:8000/article/<文章ID>/edit/ 時，將會顯示一個表單，允許用戶更新指定 ID 的文章的 title 和 content 欄位，且更新成功後重定向到名為 article_list 的 URL。**
```python
from django.views.generic import UpdateView
from .models import Article
from django.urls import reverse_lazy

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'article_form.html'
    success_url = reverse_lazy('article_list')
```
**模板範例:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Update Article</title>
</head>
<body>
    <h1>Update Article</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save changes</button>
    </form>
</body>
</html>
```
**URL配置:**
```python
from django.urls import path
from .views import ArticleUpdateView

urlpatterns = [
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
]
```


### 3.6 `DeleteView` - 刪除視圖

用於刪除資料。

#### 範例:
```python
from django.views.generic import DeleteView
from .models import Article
from django.urls import reverse_lazy

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('article_list')
```

#### **模板範例：**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Delete Article</title>
</head>
<body>
    <h1>Are you sure you want to delete this article?</h1>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Yes, delete</button>
    </form>
</body>
</html>
```

#### **URL 配置：**
```python
from django.urls import path
from .views import ArticleDeleteView

urlpatterns = [
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]
```


---

## 4. Mixin 的使用

Mixin 是 CBV 內常用的組件，允許我們添加額外的功能。

### 4.1 `LoginRequiredMixin` - 需要登入

限制未登入的使用者訪問某個視圖。

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Article

class ProtectedArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    login_url = '/accounts/login/'  # 未登入時跳轉的頁面
```

### 4.2 `PermissionRequiredMixin` - 權限檢查

限制只有特定權限的使用者才能訪問。

```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from .models import Article

class AdminArticleListView(PermissionRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    permission_required = 'app.view_article'  # 需要擁有此權限
```

---

## 5. 自定義 CBV

如果 Django 內建的 CBV 不能完全滿足需求，可以自定義 CBV。

```python
from django.views.generic import View
from django.http import JsonResponse
from .models import Article

class JsonArticleListView(View):
    def get(self, request):
        articles = list(Article.objects.values('id', 'title', 'content'))
        return JsonResponse({'articles': articles})
```

---

## 6. 總結

- CBV 讓視圖的邏輯更清晰，易於擴展和重用。
- `View` 類是所有 CBV 的基礎。
- Django 提供多種通用視圖（如 `ListView`、`DetailView`）來簡化 CRUD 操作。
- 可以透過 Mixin 增加 CBV 的功能，如登入保護。
- `as_view()` 是 CBV 與 Django URL 配置的關鍵。


