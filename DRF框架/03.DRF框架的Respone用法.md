# Django Rest Framework (DRF) - Response 用法

## 1. 引入 Response
在 DRF 中，我們需要從 rest_framework.response 模組中導入 Response 類。

```python
from rest_framework.response import Response
```
---
## 2. 基本用法
`Response` 類**接收一個 Python 對象**（如字典、列表、元組等）作為參數，並自動**將其轉換為 JSON 格式響應**。

##### 範例 1: 返回字典
```python
from rest_framework.views import APIView
from rest_framework.response import Response

class HelloWorldView(APIView):
    def get(self, request):
        data = {"message": "Hello, World!"}
        return Response(data)
```
**這會返回以下的 JSON 響應：**
```json
{
  "message": "Hello, World!"
}
```
---
## 3. 自定義狀態碼
`Response` 可以接受一個 `status` 參數來指定 HTTP 狀態碼。預設情況下，status 是 200。
可以導入`from rest_framework.response import Response` 使用現成的狀態碼

##### 範例 2: 自定義狀態碼
```python
from rest_framework.views import APIView
from rest_framework.response import Response  # 導入狀態碼庫
from rest_framework import status

class CustomStatusCodeView(APIView):
    def get(self, request):
        data = {"message": "Created successfully!"}
        return Response(data, status=status.HTTP_201_CREATED)
```

**這會返回狀態碼 201 Created 和以下 JSON 響應：**

```json
{
  "message": "Created successfully!"
}
```
---
## 4. 返回錯誤響應
當遇到錯誤時，可以使用 Response 返回錯誤信息，並自定義狀態碼。

##### 範例 3: 返回錯誤響應
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ErrorResponseView(APIView):
    def get(self, request):
        error_data = {"error": "Invalid data"}
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
```
**這會返回狀態碼 400 Bad Request 和以下錯誤信息：**
```json
{
  "error": "Invalid data"
}
```
---
## 5. 使用 data、status 和 headers
Response 還可以接受 `headers` 參數來設置**自定義的 HTTP 標頭**。

##### 範例 4: 自定義標頭
```python
from rest_framework.views import APIView
from rest_framework.response import Response

class CustomHeaderView(APIView):
    def get(self, request):
        data = {"message": "Custom header added"}
        headers = {"X-Custom-Header": "value"}
        return Response(data, headers=headers)
```
**這會在響應中添加自定義的 HTTP 標頭，並在標頭中添加 X-Custom-Header: value。
：**
```json
{
  "message": "Custom header added"
}
```
---
## 6. 包裝異常響應
DRF 提供了 `Exception` 來處理錯誤並自動返回合適的 Response。

##### 範例 5: 包裝異常響應
```py
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

class ExceptionHandlingView(APIView):
    def get(self, request):
        raise NotFound("Resource not found!")
```
**這會自動返回一個 404 Not Found 響應，並顯示錯誤信息：**
```json
{
  "detail": "Resource not found!"
}
```
---
## 7. 返回 Serializer 的數據
使用序列化器 (Serializer) 將模型數據(python)轉換為 符合 JSON 格式。Response 可以直接返回序列化後的數據。

範例 6: 返回序列化數據
```python
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()

class ItemView(APIView):
    def get(self, request):
        item = {"name": "Laptop", "price": 999.99}
        serializer = ItemSerializer(item)
        return Response(serializer.data)
```
**這會返回以下的 JSON 響應：**
```json
{
  "name": "Laptop",
  "price": 999.99
}
```
---
## 8. 返回 List 數據
若需要返回多個數據，可以使用序列化器的 `many=True` 參數來處理多個對象。

### 範例 7: 返回多個對象
```py
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()

class ItemListView(APIView):
    def get(self, request):
        items = [
            {"name": "Laptop", "price": 999.99},
            {"name": "Phone", "price": 499.99}
        ]
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
```
**這會返回以下的 JSON 響應：**
```json
[
  {
    "name": "Laptop",
    "price": 999.99
  },
  {
    "name": "Phone",
    "price": 499.99
  }
]
```
---

## 9. 總結
Response 類是 DRF 中用來返回 HTTP 響應的主要工具。
可以使用 Response 返回 JSON 格式數據、錯誤消息、狀態碼、標頭等。
支援從序列化器返回數據，並能輕鬆處理錯誤響應和異常。
