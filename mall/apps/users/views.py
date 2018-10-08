from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListCreateAPIView
# 导入:因为我们已经告知系统 子应用从app里去查找,所以就不用设置app.
# from apps.users.models import User    #错误的方式
# from users.models import User
from .models import User

# Create your views here.

# 判断用户名是否注册过
class ReigsterUserNameView(APIView):
    """判断用户名是否注册过
    1.前端用get方式把用户名传递过来
    2.后端接口设计
    GET     /users/usernames/(?P<username>\w{5,20})/count/

    拿到用户名之后,如何判断这个用户名是否注册过? 查询数据库
    """
    def get(self, request, username):
        # 满足条件的个数
        # count = 0     表示没有注册
        # count = 1     表示注册了
        # 查询用户名
        count = User.objects.filter(username=username).count()
        # 组织数据
        context = {
            'count': count,
            'username': username,
        }
        # 返回响应
        return Response(context)

# 判断手机号是否注册过
class ReigsterMoblieView(APIView):
    """
    判断手机号是否注册
    GET     /users/phones/(?P<mobile>1[345789]\d{9})/count/
    """
    def get(self, request, mobile):
        # 查询手机号
        count = User.objects.filter(mobile=mobile).count()
        # 组织数据
        context = {
            'count': count,
            'moblie': mobile,
        }
        # 返回响应
        return Response(context)
