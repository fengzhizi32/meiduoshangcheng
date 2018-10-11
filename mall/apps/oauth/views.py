import logging

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.oauth.serializers import QQRegisterSerializer
from apps.oauth.utils import OauthQQ
from .models import OAuthQQUser

# Create your views here.

class QQAuthURLView(APIView):
    """
    实现出现QQ授权登录视图
    GET /oauth/qq/statues/
    """

    def get(self,request):

        # 生成auth_url
        # https://graph.qq.com/oauth2.0/authorize
        # 请求参数请包含如下内容：
        # response_type   必须      授权类型，此值固定为“code”。
        # client_id       必须      申请QQ登录成功后，分配给应用的appid。
        # redirect_uri    必须      成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
        # state           必须      client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。请务必严格按照流程检查用户与state参数状态的绑定。
        # scope              可选      scope=get_user_info

        #获取state
        state = request.query_params.get('state')

        # #设置base_url,注意添加 ?
        # base_url = 'https://graph.qq.com/oauth2.0/authorize?'
        # #组织参数
        # params = {
        #     'response_type':'code',
        #     'client_id':settings.QQ_APP_ID,
        #     'redirect_uri':settings.QQ_REDIRECT_URL,
        #     'state':state,
        #     'scope':'get_user_info',
        # }
        #
        # #对参数进行urlencode,然后拼接url
        # auth_url = base_url + urlencode(params)

        qq = OauthQQ()
        auth_url = qq.get_oauth_url(state)

        #返回响应
        return Response({'auth_url':auth_url})

logger = logging.getLogger('meiduo')
# Create your views here.

class QQTokenView(GenericAPIView):
    """
    获取access_token
    GET /oauth/qq/users/?code=xxx
        POST /oauth/qq/users/

    """

    serializer_class = QQRegisterSerializer

    def get(self,request):

        #获取code,并进行判断
        code = request.query_params.get('code')
        if code is None:
            return Response({'message': '缺少参数'},status=status.HTTP_400_BAD_REQUEST)

        qq = OauthQQ()
        try:
            access_token = qq.get_access_token(code)
            openid = qq.get_openid(access_token)
        # except Exception as e:
        #     logger.error(e)

        except Exception:
            return Response({'message': '服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # 判断用户是否存在
        try:
            qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 不存在就是第一次授权登录
            token = OAuthQQUser.generate_save_user_token(openid)
            return Response({'access_token': token})
        else:
            # 查询用户,生成登录token
            user = qq_user.user
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })

        return Response()

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 生成已登录的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        })

        return response