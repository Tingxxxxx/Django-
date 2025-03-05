from django.contrib import admin
from django.urls import path

# 引入視圖函數或視圖類
from course.views import course_list, course_detail, CourseListView, CourseDetailView

urlpatterns = [
    # 函數式接口 Function Based View
    path('fbv/list/', course_list, name='fbv-list'),
    path('fbv/detail/<int:pk>/', course_detail, name='fbv-detail'), # 要調用哪個方法應該在http請求中做出區別，而不是在url中設定

    # 類視圖接口 Class Based View
    path('cbv/list/', CourseListView.as_view(), name='cbv-list'),
    path('cbv/detail/<int:pk>/', CourseDetailView.as_view(), name='cbv-detail'),
]
