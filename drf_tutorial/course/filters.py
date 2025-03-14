import django_filters
from .models import Course

# 自訂義一個過濾器類
class CourseFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    teacher= django_filters.CharFilter(field_name="teacher__username", lookup_expr="contains")
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr="lte")
    class Meta:
        model = Course # 關聯的模型
        fields = ['name', 'min_price', 'max_price', 'teacher']