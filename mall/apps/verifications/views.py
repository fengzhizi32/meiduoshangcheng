from django.http import HttpResponse, request
from django.shortcuts import render
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . serializers import RegisterSmsCodeSerializer
# Create your views here.



# 图片验证码
class RegisterImageCodeView(APIView):
    """
    1.前端需要一个uuid -->这个uuid用于记录图片验证码,后期用于验证
    2.生成一个图片验证码     还需要返回给我图片验证码的内容
    3.保存图片验证码
    4.返回图片

    用GET方式:     /verifications/imagecodes/(?P<image_code_id>.+)/
    """

    def get(self, request, image_code_id):
        # 1.生成一个图片验证码
        text, image = captcha.generate_captcha()
        # 2.保存图片验证码
        # 链接redis
        redis_conn = get_redis_connection('code')

        redis_conn.setex('img_%s' % image_code_id, 60, text)

        # 返回图片
        return HttpResponse(image, content_type='image/jpeg')

# 生成短信验证码
class RegisterSmsCodeView(APIView):
    """
    步骤一: 分析页面的思路逻辑(大概的步骤)
        1.当用户点击获取短信验证码按钮的时候,需要前端将: 手机号,图片验证码和uuid返回
        2.进行数据验证
        3.生成短信
        4.发送短信
        5.记录短信
        6.返回
    步骤二: 根据分析的逻辑确定:请求方式和url
        GET_方法一:    verififcations/smscodes/mobile/image_text/uuid/
        GET_方法二:    verififcations/smscodes/?mobile = xxx & image_text = xxx & uuid = xxx
        GET_方法三:    verififcations/smscodes/mobile/? image_text = xxx & uuid = xxx
    步骤三: 按照步骤实现功能
        # GET /verifications/smscodes/(?P<mobile>1[345789]\d{9})/?text=xxxx & image_code_id=xxxx
    """
    def get(self, request, mobile):

        # 1.获取参数
        query_params = request.query_params
        # 2.校验参数
        # text = query_params.get('text')
        # image_code_id = query_params.get('image_code_id')


        # 创建一个序列化器
        serializer = RegisterSmsCodeSerializer(data=query_params)
        # 验证
        serializer.is_valid(raise_exception=True)