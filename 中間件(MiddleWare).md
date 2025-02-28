# Django 中間件（Middleware）

## 1. 什麼是中間件？

中間件（Middleware）是 Django 中處理請求和響應的鉤子（hook），允許開發者在請求到達視圖之前、以及響應發送給客戶端之前進行自定義處理。

## 2. 中間件的作用

- **修改請求（Request）**：在請求到達視圖前對其進行處理，如身份驗證、日誌記錄。
- **修改響應（Response）**：在響應發送給用戶前對其進行處理，如數據壓縮、內容替換。
- **異常處理（Exception Handling）**：攔截視圖處理過程中發生的異常，進行日誌記錄或錯誤頁面處理。
- **請求與響應的全局處理**：如跨站請求（CSRF）保護、會話管理等。

## 3. Django 預設的中間件

Django 提供了一些內建的中間件，可以在 `settings.py` 的 `MIDDLEWARE` 列表中找到，例如：

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 確保請求和響應的安全性
    'django.contrib.sessions.middleware.SessionMiddleware',  # 管理會話框架的中間件
    'django.middleware.common.CommonMiddleware',  # 添加多種通用功能的中間件，例如 URL 規範化
    'django.middleware.csrf.CsrfViewMiddleware',  # 防止跨站請求偽造（CSRF）攻擊的中間件
    'django.middleware.authentication.AuthenticationMiddleware',  # 管理使用者認證的中間件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 防止點擊劫持的中間件
]

```

這些內建中間件負責處理安全性、會話管理、跨站請求保護等功能。

## 4. 自定義中間件

開發者可以自定義中間件來添加自定義功能。

### 4.1 創建自定義中間件

在 Django 項目的應用目錄下創建 `middleware.py`，並定義一個中間件類。

```python
from django.utils.deprecation import MiddlewareMixin

class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        在請求到達視圖之前執行，例如添加自定義標頭。
        """
        print("處理請求：", request.path)

    def process_response(self, request, response):
        """
        在視圖處理請求後修改響應。
        """
        print("處理響應：", response.status_code)
        return response
```

### 4.2 註冊自定義中間件

在 `settings.py` 中添加我們的自定義中間件：

```python
MIDDLEWARE += [
    'myapp.middleware.CustomMiddleware',
]
```

## 5. 中間件方法解析

Django 中間件可以實現以下方法來攔截請求和響應：

### 5.1 `process_request(self, request)`
- 在視圖處理請求之前執行。
- 可以對 `request` 進行修改。
- 若返回 `HttpResponse`，則請求直接終止，不會進入視圖。

### 5.2 `process_view(self, request, view_func, view_args, view_kwargs)`
- 在請求進入視圖前執行。
- 可以用於視圖級別的權限控制。
- 若返回 `HttpResponse`，則請求終止。

### 5.3 `process_exception(self, request, exception)`
- 當視圖拋出異常時執行。
- 可用於錯誤日誌記錄或自定義錯誤頁面。

### 5.4 `process_response(self, request, response)`
- 在視圖執行完畢後執行。
- 可以用於修改 `response`。

## 6. 總結

- **Django 中間件提供了在請求-響應處理過程中的鉤子。**
- **內建中間件負責安全、會話、跨站請求保護等功能。**
- **可以自定義中間件來添加請求過濾、響應修改、異常處理等功能。**
- **通過 `process_request`、`process_response`、`process_view`、`process_exception` 來處理請求和響應的不同階段。**

