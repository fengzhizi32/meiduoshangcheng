import logging
from urllib.parse import urlencode
from urllib.request import urlopen

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

# from .serializers import QQRegisterSerializer
from utils.exceptions import logger
from .utils import OauthQQ

from mall import settings
from .models import OauthQQUser

# Create your views here.


# 实现出现QQ授权登录视图
class QQ_OauthURLView(APIView):
    """实现出现QQ授权登录视图"""
    # GET /oauth/qq/statues/


    def get(self, request):

        # 生成auth_url
        # https://graph.qq.com/oauth2.0/authorize
        # 请求参数请包含如下内容：
        # response_type   必须      授权类型，此值固定为“code”。
        # client_id       必须      申请QQ登录成功后，分配给应用的appid。
        # redirect_uri    必须      成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
        # state           必须      client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。请务必严格按照流程检查用户与state参数状态的绑定。
        # scope              可选      scope=get_user_info

        #获取state
        # state = 'tate'
        state = request.query_params.get('state')
        #设置base_url,注意添加 ?
        # base_url = 'https://graph.qq.com/oauth2.0/authorize?'
        #组织参数
        # params = {
        #     'response_type':'code',
        #     'client_id':settings.QQ_APP_ID,
        #     'redirect_uri':settings.QQ_REDIRECT_URL,
        #     'state': state,
        #     'scope':'get_user_info',
        # }
        # http://api.meiduo.site:8000/oauth/qq/statues/?state=/
        #对参数进行urlencode,然后拼接url

        qq = OauthQQ()

        auth_url = qq.get_oauth_url(state)

        # 返回响应
        return Response({'auth_url': auth_url})


# 获取access_token
class QQ_TokenView(APIView):
    """获取access_token
    GET /oauth/qq/users/?code=xxx
    """

    def get(self, request):

        #获取code,并进行判断
        code = request.query_params.get('code')
        if code is None:
            return Response({'message': '缺少参数'}, status=status.HTTP_400_BAD_REQUEST)

        qq = OauthQQ()
        try:
            # 通过code 换access_token
            access_token = qq.get_access_token(code)
            openid =qq.get_openid(access_token)
        except Exception :
            return Response({'message': '服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


        # return response


        # 我们需要根据 openid 来进行判断
        # 如果 openid 存在于数据库中, 直接返回登陆的 token
        # 如果数据库中没有 openid ,说明用户是第一次绑定,需要跳转到 绑定页面
        try:
            qq_user = OauthQQUser.objects.get(openid = openid)
        except OauthQQUser.DoesNotExist:
            # 说明是第一次绑定,则跳转到  绑定页面
            # 需要把 openid 应该作为一个参数 传递过去
            # return Response({'openid': openid})
            # 因为 openid 非常重要,所有以需要对openid进行处理
            access_token = OauthQQUser.generate_save_user_token(openid)
            return Response({'access_token': access_token})
        else:
            # 如果openid已经在数据库中,说明已经绑定过了,直接返回登陆的token

            pass
        pass






# from itsdangerous import TimedJSONWebSignatureSerializer as S
# # s = S(scret_key = second)
# # scret_key 加密的字符串
# # second 加密的时效
# # 序列化器的初始化
# s = S('日寒月暖煎人寿', 3600)
#
# # 我们可以将 一些敏感的数据 传递给序列化器,序列化器经过一定的算法之后,会生成一个字符串
# dict = {
#     'openid': '123456789'
# }
# data = s.dumps(dict)
# data
#
# # 数据验证
# # b
# # 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzOTMyMzUxMiwiZXhwIjoxNTM5MzI3MTEyfQ
# # .eyJvcGVuaWQiOiIxMjM0NTY3ODkifQ
# # .e3ALSGzdMct0lW0ijfcJ2IKG0CcpINHdk5eadqD60Ck'
# s.loads('eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzOTMyMzUxMiwiZXhwIjoxNTM5MzI3MTEyfQ.eyJvcGVuaWQiOiIxMjM0NTY3ODkifQ.e3ALSGzdMct0lW0ijfcJ2IKG0CcpINHdk5eadqD60Ck'
# )