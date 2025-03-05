from django.contrib import admin
from django.urls import path
from course import views
urlpatterns = [
    # 函數式接口 Function Base View
    path('fbv/list/', views.course_list, name='fbv-list'),
    path('fbv/detail/<int:pk>/', views.course_detail, name='fbv-detail') # 要調用哪個方法應該在http請求中做出區別，而不是在url中設定
]
