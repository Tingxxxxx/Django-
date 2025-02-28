# Django Request 物件筆記

## 1. `request` 物件概述
在 Django 中，`request` 物件代表來自客戶端的 HTTP 請求，包含請求方法、標頭、參數、用戶資訊等。

## 2. 常見屬性與方法
### 2.1 `request.method`
- 獲取 HTTP 方法，如 `GET`、`POST` 等。
- 範例：
  ```python
  if request.method == "POST":
      print("這是一個 POST 請求")
  ```

### 2.2 `request.GET`
- 獲取 **查詢字串參數** (`?key=value` 格式)。
- `request.GET` 是一個 `QueryDict`，可用 `.get()` 取得參數。
- 範例：
  ```python
  name = request.GET.get("name", "default_value")
  print(name)  # 例如: /search?name=Django 則輸出 "Django"
  ```

### 2.3 `request.POST`
- 獲取 **表單提交的資料**。
- 只適用於 `application/x-www-form-urlencoded` 或 `multipart/form-data`。
- 範例：
  ```python
  username = request.POST.get("username")
  ```

### 2.4 `request.body`
- 獲取 **請求的原始二進位內容**，通常用於處理 JSON 或 XML 請求。
- 需手動解析，如 `json.loads(request.body)`。
- 範例：
  ```python
  import json
  data = json.loads(request.body)
  print(data)  # 若請求 body 為 {"name": "Django"}，則 data 變成 Python 字典 {"name": "Django"}
  ```

### 2.5 `request.headers`
- 獲取 **請求標頭 (Headers)**。
- 可用 `request.headers.get("Header-Name")` 取得特定標頭值。
- 範例：
  ```python
  user_agent = request.headers.get("User-Agent")
  print(user_agent)
  ```

### 2.6 `request.COOKIES`
- 獲取請求中的 **Cookies**。
- 範例：
  ```python
  session_id = request.COOKIES.get("sessionid")
  ```

### 2.7 `request.FILES`
- 獲取 **上傳的檔案**，需在 `POST` 表單中使用 `enctype="multipart/form-data"`。
- 範例：
  ```python
  uploaded_file = request.FILES.get("file")
  if uploaded_file:
      with open("uploaded_" + uploaded_file.name, "wb") as f:
          for chunk in uploaded_file.chunks():
              f.write(chunk)
  ```

### 2.8 `request.user`
- 獲取 **當前登入的用戶**，需啟用 `django.contrib.auth`。
- 若未登入，則 `request.user` 會是 `AnonymousUser`。
- 範例：
  ```python
  if request.user.is_authenticated:
      print("登入用戶：", request.user.username)
  else:
      print("使用者未登入")
  ```

### 2.9 `request.session`
- Django 內建的 **Session 機制**，可存取跨請求的數據。
- 範例：
  ```python
  request.session["user_id"] = 123
  user_id = request.session.get("user_id")
  ```

### 2.10 `request.path` 與 `request.get_full_path()`
- `request.path`：獲取請求的路徑（不包含查詢字串）。
- `request.get_full_path()`：包含查詢字串的完整 URL。
- 範例：
  ```python
  print(request.path)  # /article/5/
  print(request.get_full_path())  # /article/5/?page=2
  ```

### 2.11 `request.is_ajax()`（Django 3.1 之後已移除）
- 在 Django 3.1 以前，可以用 `request.is_ajax()` 檢查是否為 AJAX 請求。
- Django 3.1 之後，需手動檢查：
  ```python
  if request.headers.get("X-Requested-With") == "XMLHttpRequest":
      print("這是一個 AJAX 請求")
  ```

## 3. `request` 常見應用場景
### 3.1 處理 JSON 請求
```python
import json

def api_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            return JsonResponse({"message": "收到資料", "data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "無效的 JSON"}, status=400)
```

### 3.2 讀取 `GET` 參數
```python
# 當用戶訪問 http://127.0.0.1:8000/search/?q=example
def search_view(request):
    keyword = request.GET.get("q", "")
    return HttpResponse(f"搜尋關鍵字：{keyword}") # 返回:搜尋關鍵字：example
```

### 3.3 讀取 `POST` 表單數據
```python
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        return HttpResponse(f"用戶名：{username}, 密碼：{password}")
```


### 4. 總結
| **屬性 / 方法**       | **用途**                                       | **請求部分**     | **範例** |
|----------------------|----------------------------------------------|----------------|---------|
| `request.method`     | 獲取 HTTP 方法 (`GET` / `POST` / `PUT` 等)  | **請求行**     | `request.method == "POST"` |
| `request.GET`        | 取得查詢字串參數 (`?key=value`)              | **請求行**     | `request.GET.get("q")` |
| `request.POST`       | 取得表單提交數據                             | **請求體**     | `request.POST.get("username")` |
| `request.body`       | 取得請求的原始 `body`（適用 JSON、XML）      | **請求體**     | `json.loads(request.body)` |
| `request.headers`    | 取得請求標頭（Headers）                      | **請求標頭**   | `request.headers.get("User-Agent")` |
| `request.COOKIES`    | 取得 Cookies                                 | **請求標頭**   | `request.COOKIES.get("sessionid")` |
| `request.FILES`      | 取得上傳的檔案                               | **請求體**     | `request.FILES.get("file")` |
| `request.user`       | 取得當前登入用戶                             | **Session 相關** | `request.user.is_authenticated` |
| `request.session`    | 操作 Django Session                         | **Session 相關** | `request.session["key"] = value` |
| `request.path`       | 獲取請求的 URL 路徑（不含查詢字串）           | **請求行**     | `request.path == "/article/5/"` |
| `request.get_full_path()` | 獲取完整 URL（包含查詢字串）             | **請求行**     | `request.get_full_path() == "/article/5/?page=2"` |
| `request.is_ajax()`（3.1 版前） | 判斷 AJAX 請求（3.1 版後已移除） | **請求標頭**   | `request.headers.get("X-Requested-With") == "XMLHttpRequest"` |
