#coding:utf8
import json
from mall import settings
from urllib.parse import urlencode,parse_qs
from urllib.request import urlopen


class OauthQQ(object):
    ##QQ授权工具类

    def __init__(self, client_id=None, redirect_uri=None, client_secret=None,):

        self.client_id = client_id or settings.QQ_APP_ID
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URL
        self.client_secret = client_secret or settings.QQ_APP_KEY

    # 返回QQ登录网址
    def get_oauth_url(self, state):

        # 生成auth_url
        # https://graph.qq.com/oauth2.0/authorize
        # 请求参数请包含如下内容：
        # response_type   必须      授权类型，此值固定为“code”。
        # client_id       必须      申请QQ登录成功后，分配给应用的appid。
        # redirect_uri    必须      成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
        # state           必须      client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。请务必严格按照流程检查用户与state参数状态的绑定。
        # scope           可选      scope=get_user_info



        # 设置base_url,注意添加 ?
        base_url = 'https://graph.qq.com/oauth2.0/authorize?'

        # 组织参数
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': state,
            'scope': 'get_user_info',
        }

        # 对参数进行urlencode,然后拼接url
        auth_url = base_url + urlencode(params)
        return auth_url

    # 获取Access_Token
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
        # 组织参数
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        url = base_url + urlencode(params)

        # 发送请求,获取响应
        # urllib.request.urlopen(url, data=None)
        # 发送http请求，如果data为None，发送GET请求，如果data不为None，发送POST请求
        response = urlopen(url)
        'access_token=5A084A7BEE485649F0CF3001575C1F7D&expires_in=7776000&refresh_token=B70115348CB6EEF1B4F96B75160F29E5'
        # 读取数据
        data = response.read().decode()
        print('data: %s'% data)
        query_params = parse_qs(data)

        # 获取token,并进行判断
        access_token = query_params.get('access_token')
        # print(access_token)
        # ['5F5893DBC5339A54B26AFD0A1312276F']
        if access_token is None:
            raise Exception('获取token失败')

        return access_token[0]

    # 获取token之后需要获取OpenID
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

        open_url = base_url + urlencode(params)

        # urlopen(open_url) 来获取数据
        response = urlopen(open_url)
        # 读取数据
        response_data = response.read().decode()
        print(response_data)
        # callback({"client_id": "YOUR_APPID", "openid": "YOUR_OPENID"})\n;
        try:
            # 对数据进行截取,转换为字典
            data = json.loads(response_data[10:-4])
            print(data)
        except Exception :
            raise Exception('获取用户错误')

        openid = data.get('openid', None)

        return openid