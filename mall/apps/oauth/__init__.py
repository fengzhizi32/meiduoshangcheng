from django_redis.serializers import json

from mall import settings
from urllib.parse import urlencode,parse_qs
from urllib.request import urlopen


class OauthQQ(object):
    """
    QQ授权工具类
    """
    def __init__(self,client_id=None, redirect_uri=None, client_secret=None):

        self.client_id = client_id or settings.QQ_APP_ID
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URL
        self.client_secret = client_secret or settings.QQ_APP_KEY

    def get_access_token(self, code):
        # PC网站：https://graph.qq.com/oauth2.0/token
        # GET
        # grant_type      必须      授权类型，在本步骤中，此值为“authorization_code”。
        # client_id       必须      申请QQ登录成功后，分配给网站的appid。
        # client_secret   必须      申请QQ登录成功后，分配给网站的appkey。
        # code            必须      上一步返回的authorization
        # redirect_uri    必须      与上面一步中传入的redirect_uri保持一致。

        # 准备url,注意添加?
        base_url = 'https://graph.qq.com/oauth2.0/token?'
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        url = base_url + urlencode(params)

        #发送请求,获取响应
        response = urlopen(url)

        #读取数据
        data = response.read().decode()

        query_params = parse_qs(data)

        #获取token,并进行判断
        access_token = query_params.get('access_token')
        # print(access_token)
        # ['5F5893DBC5339A54B26AFD0A1312276F']
        if access_token is None:
            raise Exception('获取token失败')

        return access_token[0]

    def get_openid(self, access_token):
        # https://graph.qq.com/oauth2.0/me
        # GET
        # access_token        必须      在Step1中获取到的accesstoken。

        # 返回数据PC网站接入时，获取到用户OpenID，返回包如下：
        # callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} );
        # openid是此网站上唯一对应用户身份的标识，网站可将此ID进行存储便于用户下次登录时辨识其身份，
        # 或将其与用户在网站上的原有账号进行绑定

        base_url = 'https://graph.qq.com/oauth2.0/me?'

        params = {
            'access_token': access_token
        }

        url = base_url + urlencode(params)

        # 请求来获取响应
        response = urlopen(url)

        response_data = response.read().decode()

        try:
            # 返回的数据  callback({"client_id": "YOUR_APPID", "openid": "YOUR_OPENID"})\n;
            data = json.loads(response_data[10:-4])
        except Exception as e:
            raise Exception('获取用户错误')

        openid = data.get('openid', None)

        return openid