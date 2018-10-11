#coding:utf8
from rest_framework import serializers
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings

from oauth.models import OAuthQQUser
from users.models import User


class QQRegisterSerializer(serializers.Serializer):
    """
    创建QQ关联数据和用户模型数据
    """

    access_token = serializers.CharField(label='操作token')
    mobile = serializers.RegexField(label='手机号',regex=r'^1[345789]\d{9}$')
    password = serializers.CharField(label='密码',max_length=20,min_length=8)
    sms_code = serializers.CharField(label='短信验证码',max_length=6,min_length=6)

    def validate(self, attrs):

        #验证access_token
        access_token = attrs['access_token']
        openid = OAuthQQUser.check_save_user_token(access_token)

        if openid is None:
            raise serializers.ValidationError('无效的token')
        #注意,为attr,添加 openid数据,以备保存数据使用
        attrs['openid'] = openid


        #验证短信码
        mobile = attrs['mobile']
        redis_conn = get_redis_connection('code')

        redis_code = redis_conn.get('sms_%s'%mobile)
        if redis_code.decode() != attrs['sms_code']:
            raise serializers.ValidationError('验证码错误')

        # 判断手机号是否被注册(即 是否是注册用户)
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            pass
        else:
            #没有异常,也就是用户已经注册过
            #判断用户的密码.
            password = attrs['password']
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
            #将用户数据保存,以备保存数据使用
            attrs['user'] = user
        return attrs

    def create(self, validated_data):

        # 判断数据中是否有 user
        user = validated_data.get('user')
        if not user:
            # 不存在,就创建用户数据
            user = User.objects.create(
                username=validated_data.get('mobile'),
                password=validated_data.get('password'),
                mobile=validated_data.get('mobile')
            )
            # 修改密码
            user.set_password(validated_data['password'])
            user.save()
        # 保存QQ授权数据
        OAuthQQUser.objects.create(
            openid=validated_data.get('openid'),
            user=user
        )

        return user