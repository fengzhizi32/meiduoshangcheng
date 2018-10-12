from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from mall import settings
from utils.models import BaseModel

class OauthQQUser(BaseModel):
    """QQ登录用户数据"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)
    # db_index是个索引 快速查询数据

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name

    @staticmethod
    def generate_save_user_token(openid):

        # 实例化序列器
        serializer = Serializer(settings.SECRET_KEY, expires_in=3600)

        token = serializer.dumps({'openid': openid})

        return token.decode()

    @staticmethod
    def check_save_user_token(token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            result = serializer.loads(token)
        except BadData:
            return None

        return result.get('openid')