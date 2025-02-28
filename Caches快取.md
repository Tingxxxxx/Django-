# Django Caches 快取系統筆記

## 1. 快取概述
Django 提供內建的快取框架，允許將部分資料存儲於記憶體或其他儲存媒介中，以加速查詢與渲染頁面。

快取的優勢：
- 提高應用程式的效能
- 減少對資料庫的負擔
- 提升用戶體驗

## 2. 快取後端類型
Django 支援多種快取後端，可根據需求選擇適合的方案。

| 後端類型 | 說明 |
|----------|------|
| `django.core.cache.backends.locmem.LocMemCache` | 本機記憶體快取（單進程有效） |
| `django.core.cache.backends.filebased.FileBasedCache` | 基於文件的快取 |
| `django.core.cache.backends.db.DatabaseCache` | 使用資料庫作為快取 |
| `django.core.cache.backends.memcached.MemcachedCache` | 使用 Memcached 作為快取 |
| `django.core.cache.backends.redis.RedisCache` | 使用 Redis 作為快取（推薦） |

## 3. 設定快取
在 `settings.py` 設定快取方式。

### 3.1 使用本機記憶體快取
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

### 3.2 使用 Redis 作為快取（推薦） 
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # 1號資料庫
    }
}
```
### 3.3 儲存`session`數據到Redis快取中
- 1. 安裝所需套件: `pip install django-redis`
- 2. 配置 `settings.py`
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis 伺服器的地址和資料庫編號
        'OPTIONS': {
            # 'CLIENT_CLASS': 'django_redis.client.DefaultClient',  <--- 依redis版本不同，如果報錯此行就不要寫
            # 可選參數：設置其他 Redis 客戶端參數
            # 'SOCKET_CONNECT_TIMEOUT': 5,  # 連接超時時間（秒）
        }
    }
}

# 使用快取後端來儲存 session 數據
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default' # 指定 Django 使用哪個快取別名來存儲會話數據
```

## 4. 快取的使用
Django 提供多種快取方式，包括 API 快取、視圖快取與模板快取。

### 4.1 使用 `cache` API
```python
from django.core.cache import cache

# 設定快取
cache.set('my_key', 'Hello, Django Cache!', timeout=60)  # 60 秒後過期

# 取得快取值
value = cache.get('my_key')
print(value)  # 輸出: Hello, Django Cache!

# 刪除快取
cache.delete('my_key')
```

### 4.2 快取裝飾器（視圖快取）
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 快取 15 分鐘
def my_view(request):
    return HttpResponse("這是快取的內容！")
```

### 4.3 模板快取
Django 允許在模板中使用 `{% cache %}` 標籤來快取部分內容。
```django
{% load cache %}

{% cache 600 section_name %}
    <p>這部分的內容將被快取 10 分鐘。</p>
{% endcache %}
```

## 5. 清除快取
有時需要手動清除快取，例如更新重要數據後。

```python
from django.core.cache import cache
cache.clear()  # 清除所有快取
```

## 6. 進階快取技巧

### 6.1 低級快取 API
使用 `get_or_set` 方法來確保數據只在需要時被計算。
```python
def expensive_function():
    return "計算結果"  # 模擬高耗時計算

result = cache.get_or_set('expensive_key', expensive_function, timeout=300)
```

### 6.2 使用不同的快取
如果應用程式需要不同類型的快取，可以定義多個快取配置。
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'redis': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
    }
}
```

然後在代碼中使用特定快取：
```python
from django.core.cache import caches
redis_cache = caches['redis']
redis_cache.set('my_key', 'Redis Cache!', timeout=300)
```

## 7. 總結
- Django 支援多種快取後端，可根據需求選擇合適的方案。
- `cache` API 提供簡單的快取操作方式。
- 可使用裝飾器快取整個視圖，提高響應速度。
- 模板快取適用於部分頁面內容，減少重複渲染。
- 使用 Redis 作為快取後端可以提高效能，並適用於分佈式系統。


