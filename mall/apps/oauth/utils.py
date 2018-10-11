#coding:utf8
from mall import settings
from urllib.parse import urlencode,parse_qs
from urllib.request import urlopen


class OauthQQ(object):
    """
    QQ授权工具类
    """
    def __init__(self,client_id=None,redirect_uri=None):

        self.client_id = client_id or settings.QQ_APP_ID
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URL


    def get_oauth_url(self,state):
        # 生成auth_url
        # https://graph.qq.com/oauth2.0/authorize
        # 请求参数请包含如下内容：
        # response_type   必须      授权类型，此值固定为“code”。
        # client_id       必须      申请QQ登录成功后，分配给应用的appid。
        # redirect_uri    必须      成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
        # state           必须      client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。请务必严格按照流程检查用户与state参数状态的绑定。
        # scope              可选      scope=get_user_info


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