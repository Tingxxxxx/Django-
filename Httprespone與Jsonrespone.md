# Django `HttpResponse` 與 `JsonResponse` 筆記

在 Django 中，視圖函式（View）需要回傳 `HttpResponse` 物件，來向用戶端傳送 HTTP 回應。Django 提供了多種回應類別，其中 `HttpResponse` 與 `JsonResponse` 是最常用的兩種。

---

## 1. `HttpResponse`

`HttpResponse` 是 Django 提供的基本 HTTP 回應類別，可用來回傳純文字、HTML 或其他類型的內容。

---
### 1.1 `HttpResponse` 基本使用方式

```python
from django.http import HttpResponse

def my_view(request):
    return HttpResponse("Hello, Django!")  # 回應純文字
```
---
### 1.2 `HttpResponse` 設定 Content-Type
可以透過 content_type 參數來設定回應的 MIME 類型，例如回傳 HTML：

```python
def html_view(request):
    html_content = "<h1>這是一個 HTML 回應</h1>"
    return HttpResponse(html_content, content_type="text/html")

```
---
### 1.3 `HttpResponse` 設定狀態碼
可以使用 status 參數設定 HTTP 狀態碼，例如 404 Not Found：

```python
def not_found_view(request):
    return HttpResponse("頁面未找到", status=404)
```

---
## 2. `JsonResponse`
JsonResponse 是 Django 提供的 JSON 回應類別，專門用來返回 JSON 格式的資料，適用於 API 開發。

---
### 2.1 `JsonResponse` 基本使用方式

```python
from django.http import JsonResponse

def json_view(request):
    data = {"message": "Hello, JSON!", "status": "success"}
    return JsonResponse(data)
```
---
### 2.2 `JsonResponse` 預設行為
- Django 會自動將 Python 字典 (dict) 轉換為 JSON。內部自動執行`json.dump()`
- 預設 Content-Type 為 "application/json"。

---
### 2.3 傳回非字典類型的 JSON
如果要返回 `list` 或其他 JSON 可序列化的類型，需要將 `safe=False`，因為 `JsonResponse` 預設只允許字典：

```python
def json_list_view(request):
    data = ["apple", "banana", "cherry"]
    return JsonResponse(data, safe=False)
```
---
### 2.4 設定 JSON 回應的 HTTP 狀態碼

```python
def error_view(request):
    data = {"error": "發生錯誤", "code": 500}
    return JsonResponse(data, status=500)
```
---
### 2.5 設定 JsonResponse 為非 ASCII（防止自動轉義 Unicode）
```python
def non_ascii_json_view(request):
    data = {"message": "你好，世界！"}
    return JsonResponse(data, json_dumps_params={"ensure_ascii": False})
```
---
## 3. `HttpResponse` vs `JsonResponse` 差異對比

| 特性               | `HttpResponse`                          | `JsonResponse`                        |
|------------------|----------------------------------------|---------------------------------------|
| 回應內容格式        | 任意格式（文字、HTML、JSON等）             | JSON 格式                             |
| 預設 `Content-Type` | `text/html` 或 `text/plain`              | `application/json`                    |
| 主要用途            | 返回 HTML 或其他文本                     | 返回 JSON 格式的 API 資料              |
| 是否自動序列化      | 否，需要手動轉換為 JSON                   | 是，自動將 Python `dict` 轉換為 JSON  |
| 是否允許非 `dict`    | 是                                      | 預設不允許（除非 `safe=False`）        |


---
## 4. 適用場景
**使用 HttpResponse:**
- 返回 HTML 頁面
- 返回純文字（例如錯誤訊息）
- 需要自訂 Content-Type（如 XML、CSV）

**使用 JsonResponse**
- 提供 API 回應
- 需要回傳 JSON 資料
- 讓 Django 自動處理 JSON 序列化

---
## 5. 補充: `json.dumps()` 與 `json.loads()`

| 方法           | 作用                       | 讀/寫  | 來源        | 輸出         |
|--------------|------------------------|------|----------|------------|
| `json.dumps()` | 將 Python 物件轉換為 JSON 字串 | 寫    | Python 物件 | JSON 字串    |
| `json.loads()` | 解析 JSON 字串為 Python 物件 | 讀    | JSON 字串  | Python 物件  |
