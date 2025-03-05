from .serializers import CourseSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Course
from django.contrib.auth.models import User

"""
課程API接口的四種寫法

實現方法:
1. GET: 獲取所有課程
2. POST: 新增一個課程
3. PUT: 完整覆蓋更新一個現有的課程
4. PATCH: 僅修改課程訊息的某個欄位
5. DELETE: 刪除指定的課程
"""


"""函數式 Function Base View """
@api_view(["GET","POST"])
def course_list(request): 
    """
    獲取所有課程訊息或新增一個課程

    Args:
        resquest (_type_): 接收用戶端傳來的請求
    """ 
    # GET請求:獲取所有課程信息並回傳給用戶端
    if request.method == 'GET':
        courses = Course.objects.all() # 獲取所有課程
        s = CourseSerializer(instance=courses,many=True) # 序列化模型實例轉成Json格式
        return Response(s.data, status=status.HTTP_200_OK) 

    else: # POST請求: 接受用戶傳來的數據並新增一個課程
        s = CourseSerializer(data=request.data)  # 反序列化
        # 進行資料驗證
        if s.is_valid():
            # 驗證成功則創建並保存模型實例
            s.save(teacher=request.user) # 將講師欄設定為當前登入用戶
            return Response(s.data, status=status.HTTP_201_CREATED)
        # 驗證失敗則返回錯誤訊息
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", 'PATCH', 'DELETE'])
def course_detail(request, pk): # pk為url裡面傳遞過來的
    """
    查詢指定的課程、更新/部分更新課程訊息/刪除指定課程
    Args:
        request (_type_): 用戶端的請求
        pk (_type_): 指定課程的id
    """
    try:
         course = Course.objects.get(pk=pk) # 透過ID查詢資料庫中的指定的課程訊息

    except Course.DoesNotExist: # get方法可能會查無，故要處理異常
        return Response(data={"msg":"沒有此課程訊息"}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        # GET請求:查詢並返回指定課程訊息
        if request.method == 'GET':
            s = CourseSerializer(instance=course) # 序列化指定模型實例轉成Json格式
            return Response(s.data, status=status.HTTP_200_OK)

        # PUT請求:更新指定課程的所有訊息    
        elif request.method == "PUT":
            # 反序列化
            s = CourseSerializer(instance=course, data=request.data) # 要更新的模型為course，更新的資料為用戶傳來的request.data
            # 驗證資料
            if s.is_valid():
                # 驗證成功則updat保存e並到資料庫
                s.save() # 因更新現有資料，講師欄之前就默認為當前登入用戶，故不用像POST請求一樣新增
                return Response(data=s.data, status=status.HTTP_201_CREATED)
            # 驗證失敗則返回錯誤訊息
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST) 
        
        # PETCH請求:僅更新指定的欄位
        elif request.method == "PATCH":
            s = CourseSerializer(instance=course, data=request.data, partial=True) # 反序列化
            if s.is_valid():
                s.save()
                return Response(data=s.data, status=status.HTTP_201_CREATED)
            # 驗證失敗則返回錯誤訊息
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # DELETE請求:刪除指定課程
        else:
            course.delete() # 直接刪除該模型實例
            return Response(status=status.HTTP_204_NO_CONTENT)            


# """類視圖 Class Base View """

# """通用類視圖 Gernic Base View"""


# """視圖集 Viewset Base View"""
