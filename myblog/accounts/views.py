from django.shortcuts import render

# Create your views here.

# 登陸
def login(request):
    return render(request,'login.html')

# 註冊
def register(request):
    return render(request,'register.html')