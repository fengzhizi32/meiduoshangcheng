from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection


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
