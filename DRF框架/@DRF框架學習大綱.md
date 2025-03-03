# Django REST framework（DRF）學習路徑

## 🔰 基礎階段（入門）

### ✅ 1. Django & RESTful API 基礎  
📌 **目標**：理解 Django 基礎，掌握 RESTful API 概念  
- Django 框架基礎（Model、View、Template、ORM）
- RESTful API 概念（HTTP 方法、JSON、狀態碼）  
- 安裝 DRF 並建立 Django API 專案  
- 配置 `INSTALLED_APPS` 及 `urls.py`  

### ✅ 2. Serializer（序列化）  
📌 **目標**：學會將 Django Model 轉換為 JSON，並處理請求數據  
- `serializers.Serializer` vs `serializers.ModelSerializer`  
- 驗證 (`validate_<field_name>()` & `validate()`)  
- 自訂 `create()` 和 `update()`  

### ✅ 3. API Views（視圖）  
📌 **目標**：學會使用 DRF 提供的 API 視圖來處理請求  
- `@api_view()`（基於函式的視圖 FBV）  
- `APIView`（基於類別的視圖 CBV）  
- `GenericAPIView`（通用視圖）  
- `ListAPIView`、`RetrieveAPIView`、`CreateAPIView`  
- `UpdateAPIView`、`DestroyAPIView`、`ListCreateAPIView`  

---

## 🚀 進階階段（應用）

### ✅ 4. ViewSet & Router（視圖集合與路由）  
📌 **目標**：使用 `ViewSet` 和 `Router` 簡化 API 代碼  
- `ModelViewSet`（完整的 CRUD API）  
- `ReadOnlyModelViewSet`（僅允許讀取）  
- `DefaultRouter` 自動生成 URL 路由  

### ✅ 5. 驗證與權限（Authentication & Permission）  
📌 **目標**：確保 API 安全性  
- 內建權限類型（`IsAuthenticated`、`IsAdminUser`）  
- 自訂權限（`BasePermission`）  
- JWT 驗證（`djangorestframework-simplejwt`）  

### ✅ 6. API 進階功能（分頁、過濾、搜尋）  
📌 **目標**：優化 API 資料查詢與呈現方式  
- **分頁**：`PageNumberPagination`、`LimitOffsetPagination`、`CursorPagination`  
- **過濾**：`DjangoFilterBackend`  
- **搜尋**：`SearchFilter`、`OrderingFilter`  

---

## 🎯 高階階段（最佳化與實戰）

### ✅ 7. API 效能優化與快取  
📌 **目標**：提升 API 效能，減少數據庫查詢次數  
- **快取機制**（Redis + `cache_page`）  
- **批量查詢優化**（`select_related()`、`prefetch_related()`）  
- **異步任務處理**（Celery + DRF）  

### ✅ 8. API 測試與錯誤處理  
📌 **目標**：確保 API 穩定性，防止錯誤  
- **單元測試與 API 測試**（`pytest-django`、Postman）  
- **異常處理**（`exception_handler` 自訂錯誤格式）  

### ✅ 9. API 部署與安全性  
📌 **目標**：將 API 佈署至線上環境，確保安全  
- 使用 **Gunicorn + Nginx 部署**  
- **CORS 設定**（`django-cors-headers`）  
- **API 日誌與監控**（Sentry、Prometheus）  

---

## 📌 學習建議

### 📗 初學者建議
- 先學習 Django 基礎
- 理解 RESTful API 基本概念
- 完成一個 **簡單 CRUD API**

### 📘 進階建議
- 透過 `ViewSet` 和 `Router` 簡化 API  
- 為 API 加上 **權限控制 & JWT 驗證**  
- 加入 **分頁、搜尋、過濾** 提升 API 可用性  

### 📙 高階建議
- 優化 API 效能（快取、異步處理）  
- 測試 API，確保系統穩定  
- 部署 API，並確保其安全性  

---

## 🎯 最終目標
✅ **開發高效能 REST API**  
✅ **確保 API 安全性（身份驗證、權限控制）**  
✅ **能夠測試與部署 API 至正式環境**  

