from django.db import models
from django.contrib.auth import get_user_model

# 獲取用戶模型
User = get_user_model()

# 部落格文章的分類模型
class BlogCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='分類')

    # 設置模型的元數據
    # verbose_name 用於管理界面顯示更加友好的名稱
    class Meta:
        verbose_name = '文章分類' # 單數形式
        verbose_name_plural = verbose_name # 複數形式，使用與單數相同的名稱


    def __str__(self):
        return self.name

# 部落格文章相關的模型
class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='標題')  # 文章標題
    content = models.TextField(verbose_name='內容')  # 文章內容
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='發布時間')  # 發布時間
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')  # 作者欄使用外鍵關聯到User模型
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_DEFAULT, default=1, verbose_name='分類')  # 外鍵關聯到BlogCategor，並設置默認分類
    
    class Meta:
        verbose_name = '文章' 
        verbose_name_plural = verbose_name 
        ordering = ['-pub_time']

    def __str__(self):
        return self.title

# 文章關聯評論模型
class BlogComment(models.Model): 
    content = models.TextField(verbose_name='內容')  # 評論內容
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='發布時間')  # 評論發布時間
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')  # 發布評論的用戶
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='所屬文章', related_name='comments')  # 評論關聯的文章
    # blog外鍵 定義反向查詢模型的名稱 related_name='comments'，可透過Blog.comment 來獲取該文章的評論(取代blog.blogcomment_set)
    class Meta:
        verbose_name = '文章評論'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']

    

    def __str__(self):
        return f'Comment by {self.author} on {self.blog}'
