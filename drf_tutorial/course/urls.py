from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
# 引入視圖函數或視圖類
from course.views import *

# 快速註冊視圖集url
router = DefaultRouter()
router.register(prefix="viewset", viewset=CourseListDetailViewset) # prefix參數,URL不要加 /

urlpatterns = [
    # 函數式接口 Function Based View
    path('fbv/list/', course_list, name='fbv-list'),
    path('fbv/detail/<int:pk>/', course_detail, name='fbv-detail'),   # 要調用哪個方法應該在http請求中做出區別，而不是在url中設定

    # 類視圖接口 Class Based View
    path('cbv/list/', CourseListView.as_view(), name='cbv-list'),
    path('cbv/detail/<int:pk>/', CourseDetailView.as_view(), name='cbv-detail'),

    # 通用類視圖 Generic Based View
    path('gcbv/list/', GCourseListView.as_view(), name='gcbv-list'),
    path('gcbv/detail/<int:pk>', GCourseDetailView.as_view(), name='gcbv-detail'),

    # 視圖集 Viewset 使用router快速註冊
    path("", include(router.urls))

    # # 視圖集 Viewset 指定調用方法
    # path('viewset/list/', CourseListDetailViewset.as_view(
    #     {'get': 'list', 'post': 'create'}
    # )),
    # path('viewset/detail/<int:pk>/', CourseListDetailViewset.as_view(
    #     {'get': 'retrieve', 'put': 'update',
    #         'patch': 'partial_update', 'delete': 'destroy'}
    # ))
]