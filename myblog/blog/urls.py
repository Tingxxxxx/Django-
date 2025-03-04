from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('blog/pub', views.pub_blog, name='pub_blog'),
    path('blog/comment', views.pub_comment, name='pub_comment'),
    path('blog/search', views.search_blog, name='search_blog'),
    path('blog/upload_image/', views.upload_image, name='upload_image'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
