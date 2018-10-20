from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from goods.serializers import SUKSerializer
from .models import User
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import CreateAPIView
from .serializers import RegisterCreateUserSerializer, UserCenterInfoSerializer, EmailSerializer, AddressSerializer, \
    UserHistorySerializer

# 导入:因为我们已经告知系统 子应用从app里去查找,所以就不用设置app.
# from apps.users.models import User    #错误的方式
# from users.models import User

# Create your views here.
"""
APIView                 基类
GenericAPIView          列表,详情 做了通用支持,queryset, serializer_class
ListAPIView             queryset, serializer_class  http的方法都可以不写
"""

# 判断用户名是否注册过
class RegisterUserNameView(APIView):
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
class RegisterMoblieView(APIView):
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

# 实现注册功能    数据入库(使用  CreateAPIView里的POST方法)
class RegisterCreateUserView(APIView):
    """实现注册功能

    POST

    1.我们需要前端把:用户名,密码1,密码2,手机号,短信验证码,是否同意,提交给后台
    2.对数据进行校验
    3.数据入库
    """

    serializer_class = RegisterCreateUserSerializer

    def post(self, request):

        # 1.接收参数
        data = request.data

        # 2.创建序列化器
        serializer = RegisterCreateUserSerializer(data=data)

        # 校验
        serializer.is_valid(raise_exception=True)

        # 3.入库
        serializer.save()

        # 4.返回响应
        return Response(serializer.data)


# 用户中心个人信息
""" APIView 方法 """
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
# class UserCenterInfoView(APIView):
#     """
#     获取登录用户的信息
#     GET /users/infos/
#     既然是登录用户,我们就要用到权限管理
#     在类视图对象中也保存了请求对象request
#     request对象的user属性是通过认证检验之后的请求用户对象
#     """
#
#     # 指定的视图中    设置权限
#     # IsAuthenticated  登陆用户(认证用户)
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#
#         # 1.获取用户信息
#         # 我们采用的是 jwt token 认证,只要前端传递的token是正确的, 就可以确认
#         # 登录用户 保存在request.user中
#         user = request.user
#
#         # 2.创建序列化器
#         serializer = UserCenterInfoSerializer(user)
#
#         # 3.返回响应
#         return Response(serializer.data)

""" GenericAPIView 方法 """
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
# class UserCenterInfoView(RetrieveModelMixin, GenericAPIView):
#
#     # 设置序列化器
#     serializer_class = UserCenterInfoSerializer
#
#     # 默认如果是根据 pk 来获取数据的时候   需要设置    这个属性
#     # queryset = User.objects.all()
#
#     def get_object(self):
#
#         return self.request.user
#
#     def get(self, request):
#
#         return self.retrieve(request)

""" RetrieveAPIView 方法 """
from rest_framework.generics import RetrieveAPIView
class UserCenterInfoView(RetrieveAPIView):

    serializer_class = UserCenterInfoSerializer

    def get_object(self):

        return self.request.user

# 邮箱验证
""" APIView """
# class UserEmailView(APIView):
#     """
#     必须用户登录才可以设置
#     1.当用户输入邮箱内容 点击保存的时候, 前端发送请求给后端
#     2.后端接收到数据之后, 更新数据库
#     3.给邮箱发送一条激活邮件
#     4.返回响应
#
#     PUT     /users/emails/
#     """
#
#     permission_classes = [IsAuthenticated]
#
#     def put(self, request):
#
#         # 1.接收数据
#         data = request.data
#         user = request.user
#
#         # 2.对数据进行校验
#         serializer = EmailSerializer(instance=user, data=data)
#         serializer.is_valid(raise_exception=True)
#
#         # 3.更新数据
#         serializer.save()
#
#         # 4.发送激活邮件
#
#
#         # 5.返回响应
#         return Response(serializer.data)

""" UpdateAPIView """
from rest_framework.generics import UpdateAPIView

class UserEmailView(UpdateAPIView):

    serializer_class = EmailSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):

        return self.request.user


from rest_framework import status
class UserEmailActiveView(APIView):

    def get(self, request):

        # 获取token
        token = request.query_params.get('token')
        # 判断token是否存在
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 对token进行loads操作
        user = User.check_verify_token(token)
        if user is  None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 修改用户的email_active状态
        user.email_active = True
        user.save()
        return Response({'message': 'ok'})


# 地址
class AddressView(APIView):
    """
    POST    users/addresses/
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        1.接收前端提交的数据
        2.对数据进行校验
        3.保存数据
        4.返回响应
        """
        data = request.data

        serializer = AddressSerializer(data=data, context={'request': request})

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


# 我们只记录: 登录用户的浏览记录

# 1.哪里添加? 哪里记录? 在用户中心
# 用户在登录之后 访问详情页面的时候 需要让前端发送一个请求
# 这个请求包含:这个请求包含 商品ID 和用户信息(token)
# 后端接收数据
# 添加浏览记录[数据库,redis中] 选择存储在redis 中
# 返回响应

class UserHistoryView(APIView):
    """
    POST    /user/browerhistories/
    """
    # 用户为登陆状态
    permission_classes = [IsAuthenticated]
    # 采用jwt进行验证, 前端在传递 商品id 和 token的时候
    # token 会在 请求的header中添加
    # 商品id 会在 请求的body中添加

    def post(self, request):

        # 1.接收数据
        data = request.data
        # 2.通过序列化器校验
        serializer = UserHistorySerializer(data=data)
        serializer.is_valid(raise_exception=True)

        sku_id = serializer.validated_data.get('sku_id')
         # 3.数据入库    Redis的什么类型数据中--->列表实现
            # 连接redis
        redis_conn = get_redis_connection('history')
            # 添加到redis中, 先把已经存在的商品id删除
        redis_conn.lrem('history_%s' % request.user.id, 0, sku_id)
            # 再添加
        redis_conn.lpush('history_%d' % request.user.id, sku_id)
            # 截取列表的前五个
        redis_conn.ltrim('history_%s' % request.user.id, 0, 4)
        print(serializer.data)
        # 4.返回
        return Response(serializer.data)

    def get(self, request):

        # 1.用户信息已经检验, 因为已经添加了权限
        # 2.得到用户的 id
        user_id = request.user.id
        # 3.连接到redis 获取 sku_id
        redis_conn = get_redis_connection('history')
        sku_ids = redis_conn.lrange('history_%s'%user_id, 0, 5)
        # 4.[1, 2, 3] 根据id获取商品的详细信息

        # skus = SKU.objects.filter(id__in=sku_ids)   # id 查询会出现数据顺序错误

        skus = []
        for sku_id in sku_ids:
            sku = SKU.objects.get(pk = sku_id)
            skus.append(sku)

        # 5.[SKU, SKU, SKU] 需要将对象列表转换为 字典
        serializer = SUKSerializer(skus, many=True)
        # 6.返回数据
        print(serializer.data)
        return Response(serializer.data)











