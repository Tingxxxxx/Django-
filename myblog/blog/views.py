from django.shortcuts import render

# Create your views here.

# 首頁
def index(request):
    return render(request,'index.html')

# 文章詳情
def blog_detail(request,blog_id):
    return render(request,'blog_detail.html')

# 發布文章
def pub_blog(request):
    return render(request,'pub_blog.html')
