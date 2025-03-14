# Django REST Framework 過濾組件筆記
## 1. 介紹
在 Django REST Framework (DRF) 中，過濾組件（filtering）允許我們根據查詢參數來過濾 API 返回的數據。這樣可以讓 API 更加靈活且符合用戶需求。

---
## 2. 安裝 django-filter
**確保安裝了 django-filter 套件：**
```bash
    pip install django-filter
```
**在 Django 項目的 settings.py 文件中添加 django_filters：**

```python
    INSTALLED_APPS = [
        ...
        'django_filters',
    ]
```
##　3. 設定過濾後端
**在 settings.py 中設置過濾後端：**
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
```
這樣設置後，Django REST Framework 就會自動使用 django_filters 提供的過濾功能來處理查詢參數。

---
##　4.  DRF 框架 過濾組件的基本使用
- 在視圖中使用 `filterset_fields` **來指定可以過濾的欄位。**
- 該過濾欄位的查詢條件默認為**精準匹配(exact)**
- `filterset_fields`也可指定跨欄位篩選，常用於篩選外鍵欄位

**範例1：假設有一個 Course 模型，並希望能夠根據 name、category 和 level 來過濾課程。**
```python
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course
from .serializers import CourseSerializer

# 課程訊息視圖
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()  # 查詢所有課程
    serializer_class = CourseSerializer  # 使用課程的序列化器
    filter_backends = [DjangoFilterBackend]  # 指定過濾後端
    filterset_fields = ['name', 'category', 'level']  # 設置可過濾的欄位

```
**使用: 返回 name 包含 "Python" 且 level 為 "beginner" 的課程：**

`GET /api/courses/?name=Python&level=beginner`


**範例2：假設有一個 Course 模型，並希望能夠根據 外鍵 teacher、 name 查詢資料。**
```python
# 課程信息模型類
class Course(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text='課程名稱', verbose_name='課程名稱')
    introduction = models.TextField(help_text='課程介紹', verbose_name='課程介紹')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, help_text='講師', verbose_name='講師')
    price = models.DecimalField(max_digits=6,decimal_places=2, help_text='價格', verbose_name='課程價格')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間') 

# 課程訊息的序列化器
class CourseSerializer(serializers.ModelSerializer):
    # 複寫 課程模型中的 teacher 欄位，指定source參數來獲取老師名，並設為只讀
    teacher = serializers.CharField(source='teacher.username', read_only=True)  # teacher外鍵關聯到User模型，並通過.username獲取值
    
    class Meta:
        model = Course
        fields = "__all__" 

# 用戶模型的序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
```
**在視圖中使用 `filterset_fields` 來指定可以過濾的欄位,可用於精準匹配欄位、或外鍵關聯欄位。**
```python
class CourseListDetailViewset(viewsets.ModelViewSet):
    queryset = Course.objects.all()  # 指定查詢集
    serializer_class = CourseSerializer  # 
    
    # 簡單指定過濾器欄位，可用於外鍵跨欄位過濾，或一般欄位精準匹配
    filterset_fields = ['teacher__username', 'name']  # 注意 在瀏覽器傳參時要完全按照這行的欄位名ex:?teacher__username=....
    
    def perform_create(self, serializer): # 重寫POST請求調用的方法
        serializer.save(teacher=self.request.user) # 加入講師欄
```
**使用: 返回 name 包含 "Python" 且 teacher 為 "admin" 的課程：**
`GET /api/courses/?name=Python&teacher__username=admin`


---
## 5. DRF 框架 自訂義 FilterSet類
- 自訂義過濾器類先導包`import django_filters`
- 自訂義FilterSet類需繼承自`django_filters.rest_framework.FilterSet`
- 過濾器類中，可指定`field_name`定義可篩選的欄位
- 過濾器類中，可使用`lookup_expr`參數，來指定查詢條件(例:`contains`、`iexact`、`gt`....等查詢條件)。
- 在過濾器類中，在Meta元類中使用`model`關聯要篩選的模型
- 在視圖中則通過指定`filterset_class` 來使用自訂義的FilterSet類
- 在views.py中記得先導入必要過濾組件
    - `from django_filters.rest_framework import DjangoFilterBackend`
    
**範例：假設我們希望能根據課程名稱進行模糊查詢，並能根據 price 範圍來過濾課程。**

```python
import django_filters
from .models import Course

class CourseFilter(django_filters.rest_framework.FilterSet):   
    # name 欄位進行模糊查詢，使用 `icontains` 查詢（不區分大小寫）
    name = django_filters.CharFilter(lookup_expr='icontains')  
    # price 範圍過濾，設定最小價格與最大價格過濾條件
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')  # price >= min_price
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')  # price <= max_price

    class Meta:
        model = Course  # 關聯 Course 模型進行過濾
        fields = ['name', 'min_price', 'max_price', 'category', 'level']  # 指定過濾欄位
```
**在視圖中通過`filterset_class`使用這個自訂義的過濾器：**

```python
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend # 導入過濾後端
from .models import Course
from .serializers import CourseSerializer
from .filters import CourseFilter  # 引入自訂義過濾器

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()  # 查詢所有課程
    serializer_class = CourseSerializer  # 使用課程的序列化器
    filter_backends = [DjangoFilterBackend]  # 指定過濾後端
    filterset_class = CourseFilter  # 使用自訂義過濾器
```
**在 URL 中就可以就能同時根據課程名稱、價格範圍、類別和級別進行過濾：**

`GET /api/courses/?name=Python&min_price=10&max_price=100&category=Programming&level=beginner`

---
## 6. 自訂義 FilterSet 中的過濾方法
可以在 FilterSet 類中定義一個**自訂義的方法，然後在過濾器中使用** `method` 參數**來引用這個方法。**

**範例：假設想要根據一個範圍字串過濾價格（例如，price_range=10,100）：**

```python
import django_filters
from .models import Course

class CourseFilter(django_filters.rest_framework.FilterSet):
    # price_range 使用自訂義過濾方法
    price_range = django_filters.CharFilter(method='filter_by_price_range') # 不用`lookup_expr`, 而是使用`method`來指定自訂義過濾方法


    class Meta:
        model = Course # 過濾器關聯Course模型 
        fields = ['name', 'price_range', 'category', 'level'] # 指定過濾欄位

    # 自訂義過濾方法，解析傳入的範圍字串並根據其過濾
    def filter_by_price_range(self, queryset, name, value):
        min_price, max_price = value.split(',')  # 把範圍字串拆分成最小價與最大價
        return queryset.filter(price__gte=min_price, price__lte=max_price)  # 根據價格範圍過濾課程
```
**在視圖中通過`filterset_class`使用這個自訂義的過濾器：**
```python
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course
from .serializers import CourseSerializer
from .filters import CourseFilter  # 引入自訂義過濾器

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()  # 查詢所有課程
    serializer_class = CourseSerializer  # 使用課程的序列化器
    filter_backends = [DjangoFilterBackend]  # 指定過濾後端
    filterset_class = CourseFilter  # 指定過濾類
```
**這樣這會返回所有價格在 10 到 100 之間的課程：**

`GET /api/courses/?price_range=10,100`

---
## 7. DRF django-filter 過濾器類型 
| 欄位種類                  | 描述 |
|--------------------------|---------------------------------------------------------------|
| `CharFilter`             | 用於過濾字符型欄位，例如名稱或標題。 |
| `NumberFilter`           | 用於過濾數值型欄位，例如價格或數量。 |
| `BooleanFilter`          | 用於過濾布林值欄位，例如是否激活。 |
| `DateFilter`             | 用於過濾日期型欄位，例如創建日期。 |
| `DateTimeFilter`         | 用於過濾日期時間型欄位，例如最後更新時間。 |
| `TimeFilter`             | 用於過濾時間型欄位，例如某個特定的時間點。 |
| `ChoiceFilter`           | 用於過濾選擇型欄位，例如狀態。 |
| `MultipleChoiceFilter`   | 用於過濾多選型欄位，例如多個標籤。 |
| `RangeFilter`            | 用於過濾一個範圍內的數值，例如價格範圍。 |
| `LookupChoiceFilter`     | 用於過濾有多個查詢條件的欄位，例如字段在範圍內或包含某字符串。 |
| `UUIDFilter`            | 用於過濾 UUID 欄位，例如唯一識別碼（UUID）。 |
| `AllValuesFilter`       | 用於過濾該欄位的所有可能值，類似於 `ChoiceFilter`，但值來源於資料庫中的現有數據。 |
| `ModelChoiceFilter`      | 用於過濾與外鍵（ForeignKey）關聯的對象，例如選擇某個作者的所有文章。 |
| `ModelMultipleChoiceFilter` | 用於過濾與多對多關聯（ManyToManyField）的對象，例如選擇包含某些標籤的文章。 |
| `OrderingFilter`         | 用於允許根據特定欄位進行排序，例如 `?ordering=-created_at` 來按照 `created_at` 逆序排列。 |
| `IsoDateTimeFilter`      | 專門用於 ISO 8601 格式的日期時間過濾，例如 `2023-01-01T12:00:00Z`。 |
| `NumericRangeFilter`     | 用於 PostgreSQL `numrange`、`int4range` 等範圍型欄位的過濾。 |
| `TypedChoiceFilter`      | 類似於 `ChoiceFilter`，但允許指定 `coerce` 參數來轉換數據類型，例如將輸入值轉換為整數或布林值。 |
| `BaseInFilter`           | 允許使用 `in` 查詢，例如 `id__in=[1,2,3]`。 |
| `BaseRangeFilter`        | 允許使用範圍查詢，例如 `price__range=(10,100)`。 |
| `AllValuesMultipleFilter` | 與 `AllValuesFilter` 類似，但允許過濾多個值。 |



<br>

**示例:RangeFilter 快速實現範圍查詢** 
```python
# 自訂義過濾器類，然後指定視圖中使用
class ProductFilter(django_filters.FilterSet):
    # 方式1: 瀏覽器輸入預設的 ?price_min=&price_max= 來查詢
    price = django_filters.RangeFilter() 

    # 方式2: 指定欄位名並搭配lookup_expr , 瀏覽器可用`?price=100,500` 格式
    price = django_filters.RangeFilter(field_name="price", lookup_expr="range")

    class Meta:
        model = Product
        fields = ['price']
```
**瀏覽器發送請求，RangeFilter 預設的查詢參數是 price_min 和 price_max**
`GET /api/products/?price_min=100&price_max=500`

**如果定義過濾器類時有指定欄位名，並搭配`lookup_expt="range"`**
`GET /api/products/?price=100,500`

---
## 補充: 可搭配`lookup_expr`使用的查詢條件

| 查詢條件       | 描述                              | 範例                                  | 說明                                                   |
| -------------- | --------------------------------- | ------------------------------------- | ------------------------------------------------------ |
| `exact`        | 精確匹配                           | `name=Python`                         | 精確匹配欄位的值。                                     |
| `iexact`       | 不區分大小寫的精確匹配             | `name=python`                         | 不區分大小寫，對欄位值進行精確匹配。                   |
| `contains`     | 包含                               | `name__contains=Py`                   | 查找欄位中是否包含給定的子字符串。                     |
| `icontains`    | 不區分大小寫的包含                 | `name__icontains=py`                  | 不區分大小寫，查找欄位中是否包含給定的子字符串。       |
| `gt`           | 大於                               | `price__gt=50`                        | 查詢欄位是否大於指定值。                               |
| `gte`          | 大於等於                           | `price__gte=50`                       | 查詢欄位是否大於或等於指定值。                         |
| `lt`           | 小於                               | `price__lt=100`                       | 查詢欄位是否小於指定值。                               |
| `lte`          | 小於等於                           | `price__lte=100`                      | 查詢欄位是否小於或等於指定值。                         |
| `startswith`   | 以...開頭                          | `name__startswith=Py`                 | 查詢欄位是否以指定字符串開頭。                         |
| `istartswith`  | 不區分大小寫的以...開頭            | `name__istartswith=py`                | 不區分大小寫，查詢欄位是否以指定字符串開頭。           |
| `endswith`     | 以...結尾                          | `name__endswith=on`                   | 查詢欄位是否以指定字符串結尾。                         |
| `iendswith`    | 不區分大小寫的以...結尾            | `name__iendswith=on`                  | 不區分大小寫，查詢欄位是否以指定字符串結尾。           |
| `in`           | 是否在一個給定的集合中             | `id__in=1,2,3`                        | 查詢欄位值是否在一個指定的集合內。                     |
| `isnull`       | 檢查欄位是否為 NULL                 | `field__isnull=true`                  | 查詢欄位值是否為 NULL。                                 |
| `range`        | 在一個範圍內                       | `price__range=10,100`                 | 查詢欄位值是否在一個範圍內（包含範圍的兩端）。         |
| `year`         | 年份查詢（適用於日期欄位）         | `date__year=2021`                     | 查詢日期欄位中的年份。                                 |
| `month`        | 月份查詢（適用於日期欄位）         | `date__month=5`                       | 查詢日期欄位中的月份。                                 |
| `day`          | 日查詢（適用於日期欄位）           | `date__day=10`                        | 查詢日期欄位中的日。                                   |
| `hour`         | 小時查詢（適用於時間欄位）         | `time__hour=10`                       | 查詢時間欄位中的小時。                                 |
| `minute`       | 分鐘查詢（適用於時間欄位）         | `time__minute=30`                     | 查詢時間欄位中的分鐘。                                 |
| `second`       | 秒查詢（適用於時間欄位）           | `time__second=15`                     | 查詢時間欄位中的秒。                                   |
| `is`           | 比較布林值（等於 True 或 False）    | `active__is=true`                     | 查詢欄位值是否為 True 或 False。                        |


