from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, APIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from .permissions import IsOwner
from .models import Course
from .serializers import CourseSerializer

"""
課程API接口的四種寫法:
1. 函數式FBV
2. 類視圖CBV
3. 通用類視圖GCBV
4. 視圖集Viewset

實現方法:
1. GET: 獲取所有課程
2. POST: 新增一個課程
3. PUT: 完整覆蓋更新一個現有的課程
4. PATCH: 僅修改課程訊息的某個欄位
5. DELETE: 刪除指定的課程

# 認證:
使用Django的信號機制與@reciver裝飾器，實現創建用戶自動生成token
"""


"""自動生成TOKEN函數"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User) # sender=發送信號的模型類
def create_token(sender, instance=None, created=False, **kwargs):
    """創建用戶時自動觸發函數並生成token"""
    if created:
        Token.objects.create(user=instance) # 用傳進來的User實例，在Token 表使用.create()方法創建並保存


"""函數式 Function Base View """

@authentication_classes([TokenAuthentication]) # 限制只能用token驗證
@api_view(["GET", "POST"])
def course_list(request):
    """
    獲取所有課程訊息或新增一個課程

    Args:
        resquest (_type_): 接收用戶端傳來的請求
    """
    # GET請求:獲取所有課程信息並回傳給用戶端
    if request.method == 'GET':
        courses = Course.objects.all()  # 獲取所有課程
        s = CourseSerializer(instance=courses, many=True)  # 序列化模型實例轉成Json格式
        return Response(s.data, status=status.HTTP_200_OK)

    else:  # POST請求: 接受用戶傳來的數據並新增一個課程
        s = CourseSerializer(data=request.data)  # 反序列化
        # 進行資料驗證
        if s.is_valid():
            # 驗證成功則創建並保存模型實例
            s.save(teacher=request.user)  # 將講師欄設定為當前登入用戶
            return Response(s.data, status=status.HTTP_201_CREATED)
        # 驗證失敗則返回錯誤訊息
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", 'PATCH', 'DELETE'])
def course_detail(request, pk):  # pk為url裡面傳遞過來的
    """
    查詢指定的課程、更新/部分更新課程訊息/刪除指定課程
    Args:
        request (_type_): 用戶端的請求
        pk (_type_): 指定課程的id
    """
    try:
        course = Course.objects.get(pk=pk)  # 透過ID查詢資料庫中的指定的課程訊息

    except Course.DoesNotExist:  # get方法可能會查無，故要處理異常
        return Response(data={"msg": "沒有此課程訊息"}, status=status.HTTP_404_NOT_FOUND)

    else:
        # GET請求:查詢並返回指定課程訊息
        if request.method == 'GET':
            s = CourseSerializer(instance=course)  # 序列化指定模型實例轉成Json格式
            return Response(s.data, status=status.HTTP_200_OK)

        # PUT請求:更新指定課程的所有訊息
        elif request.method == "PUT":
            # 要更新的模型為course，更新的資料為用戶傳來的request.data
            s = CourseSerializer(instance=course, data=request.data)  # 反序列化

            # 驗證資料
            if s.is_valid():
                # 驗證成功則updat保存e並到資料庫
                s.save()  # 因更新現有資料，講師欄之前就默認為當前登入用戶，故不用像POST請求一樣新增
                return Response(data=s.data, status=status.HTTP_200_OK)
            # 驗證失敗則返回錯誤訊息
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

        # PETCH請求:僅更新指定的欄位
        elif request.method == "PATCH":
            s = CourseSerializer(
                instance=course, data=request.data, partial=True)  # 反序列化
            if s.is_valid():
                s.save()
                return Response(data=s.data, status=status.HTTP_200_OK)
            # 驗證失敗則返回錯誤訊息
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

        # DELETE請求:刪除指定課程
        else:
            course.delete()  # 直接刪除該模型實例
            return Response(status=status.HTTP_204_NO_CONTENT)


"""類視圖 Class Based View """
class CourseListView(APIView):
    # 指定驗證方式
    authentication_classes = (TokenAuthentication, BasicAuthentication)  
    def get(self, request):
        """獲取所有課程資料"""
        courses = Course.objects.all()
        s = CourseSerializer(instance=courses, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)

    def post(self, request):
        """新增一個課程"""
        s = CourseSerializer(data=request.data)  # 接收用戶傳來的資料進行反序列化
        if s.is_valid():  # 驗證資料
            s.save(teacher=self.request.user)  # 因為是類，故記得加self
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    # 指定驗證方式
    # authentication_classes = ()
    @staticmethod
    def get_obj(pk):
        """獲取指定的課程模型實例"""
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise NotFound("Course not found")  # 拋出NotFoun異常

    def get(self, request, pk):
        """查詢指定課程"""
        course = self.get_obj(pk=pk)  # 獲取模型實例
        s = CourseSerializer(instance=course)
        return Response(data=s.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        """更新指定課程"""
        course = self.get_obj(pk=pk)  # 獲取模型實例
        s = CourseSerializer(instance=course, data=request.data)  # 序列化模型實例
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_200_OK)
        raise ValidationError(s.errors)  # 抛出ValidationError異常

    def patch(self, request, pk):
        """更新指定課程（部分更新）"""
        course = self.get_obj(pk=pk)
        s = CourseSerializer(instance=course, data=request.data, partial=True)  # 反序列化
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_200_OK)
        raise ValidationError(s.errors)  # 抛出ValidationError异常

    def delete(self, request, pk):
        """刪除指定課程"""
        course = self.get_obj(pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



"""通用類視圖 Generic Based View"""
class GCourseListView(generics.ListCreateAPIView): # ListCreateAPIView 提供GET與POST請求
    # 指定驗證方式
    # authentication_classes = ()
    # 覆寫父類屬性，注意:前面的屬性名是固定的
    queryset = Course.objects.all() # 指定查詢集
    serializer_class = CourseSerializer # 指定序列化器
    def perform_create(self, serializer):  # 覆寫父類POST請求時調用的方法
        serializer.save(teacher=self.request.user) # 加入講師欄

class GCourseDetailView(generics.RetrieveUpdateDestroyAPIView): # 提供GET(查指定)、PUT、PATCH、DELETE
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


"""視圖集 Viewset"""
class CourseListDetailViewset(viewsets.ModelViewSet):
    # 指定驗證方式
    authentication_classes = [BasicAuthentication, TokenAuthentication] # 注意元組中只有一個值加,或者使用[]
    # 指定自訂的權限類，僅有對像擁有者可訪問
    permission_classes = [IsOwner]
    queryset = Course.objects.all()  # 指定查詢集
    serializer_class = CourseSerializer  # 指定序列化器

    def perform_create(self, serializer): # 重寫POST請求調用的方法
        serializer.save(teacher=self.request.user) # 加入講師欄

    
    