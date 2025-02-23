from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST,require_GET
from django.urls import reverse, reverse_lazy
from .form import PubBlogForm, PubCommentForm
from .models import Blog,BlogCategory,BlogComment
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import os
# Create your views here.

# 首頁
def index(request):
    blogs = Blog.objects.all()
    return render(request,'index.html', context={'blogs':blogs})

# 文章詳情
def blog_detail(request,blog_id):
    # get()如果找不到會報錯,故通常會放在try中
    try:
        blog = Blog.objects.get(pk=blog_id)
    # 實際業務中這裡可以返回一個404notfound之類的頁面
    except Exception as e:
        blog = None  
    return render(request,'blog_detail.html', context={'blog':blog})

@require_http_methods(['GET','POST'])
# 發布文章
@login_required(login_url=reverse_lazy('accounts:login'))
def pub_blog(request):
    if request.method == 'GET':
        categorys = BlogCategory.objects.all()
        return render(request,'pub_blog.html', context={'categorys':categorys})
    
    # post請求
    else:
        form = PubBlogForm(request.POST)
        # 表單驗證成功
        if form.is_valid():
            print('表單驗證成功')
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id  = form.cleaned_data.get('category') # 文章實例中的分類僅存id,外鍵關聯到分類表
            # 保存文章到資料庫
            # 用 category_id(資料庫的分類表的id欄位) = category_id，即文章表中有一個外鍵，關聯到分類表的主鍵id
            blog = Blog.objects.create(title=title, content=content, category_id = category_id, author= request.user)
            return JsonResponse({'code':200, 'message':'文章發布成功', "data":{'blog_id':blog.id}})
        #　表單驗證失敗
        else:
            print(form.errors)
            return JsonResponse({'code':400, 'message':'文章發布失敗'})

@require_POST # 只接收POST請求
@login_required # 必須登入才能評論
# 評論視圖
def pub_comment(request):
    form = PubCommentForm(request.POST)
    if form.is_valid():
        blog_id = request.POST.get('blog_id') # 評論關聯的文章ID，在前端文章詳情頁新增一個隱藏的input標籤來提供
        content = form.cleaned_data.get('content') # 獲取評論內容
        # 保存評論到資料庫
        BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
        # 重新加載該文章頁面來返回評論
        return redirect(reverse('blog:blog_detail',kwargs={"blog_id":blog_id}) )
    # 確保表單驗證失敗也會刷新頁面
    return redirect(reverse('blog:blog_detail',kwargs={"blog_id":blog_id}) )
    # redirect()傳參要直接通過關鍵字參數，不能用kwargs={:}
    # redirect() 會自動處理 URL 反轉，一般刷新頁面會跳轉 redirect('blog:blog_detail') 這樣即可，不用加reverse
    # reverse() 主要用於 非重定向情況下動態生成 URL,用於其他操作或傳遞給模板時


@require_GET 
# 文章搜索功能(僅搜索，不涉及變更，故一般用GET即可)
# 用戶在搜索框輸入的內容，會通過查詢字符串傳遞EX: /blog/search_blog/?search=Python
def search_blog(request):
    search = request.GET.get('search', '').strip() # 使用使用strip()去除用戶可能誤輸的空格
    if search:
        blogs = Blog.objects.filter(
            Q(title__icontains=search)|
            Q(content__icontains=search))
        return render(request,'index.html',context={'blogs':blogs})
    else:
        # 如果輸入空白，則跳轉首頁
        return redirect("/")






import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        # 打印返回的URL以調試
        url = settings.MEDIA_URL + 'uploads/' + image.name
        print(f'Returning URL: {url}')
        return JsonResponse({'data': {'url': url}})
    return JsonResponse({'error': 'Upload failed'}, status=400)
