import re
from users.models import User
from django.contrib.auth.backends import ModelBackend


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义jwt认证成功后返回的数据"""

    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

# 定义一个方法,根据 正则来匹配手机号,如果不满足手机号就是用户名
def get_user_by_account(account):

    try:
        # 如果用户输入是手机号的正则
        if re.match(r'1[345789]\d{9}',account):
            # 执行手机号登陆
            user = User.objects.get(mobile=account)
        else:
            # 否则,执行用户名登录
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        user = None

    return user

# ModelBackend 为什么继承自它
# 都是因为懒, 这样可以少写一个方法
class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户名或手机号认证"""

    # 如果用户输入手机号,我们需要通过手机号 查找到该用户
    # 然后再通过该用户校验密码
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 得到用户
        user = get_user_by_account(username)

        if user is not None and user.check_password(password):
            return user
        else:
            return None
