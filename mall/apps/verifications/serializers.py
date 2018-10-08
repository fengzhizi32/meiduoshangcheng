# coding:utf8
from rest_framework import serializers
from django_redis import get_redis_connection
# 序列化器:

# 短信验证码
class RegisterSmsCodeSerializer(serializers.Serializer):
    """
    数据验证的方法:
    1.UUIDField字段类型验证
    2.max_length = 4 选项验证
    3.单个字段验证
    4.多个字段验证
    """
    # 用户输入的图片验证码
    text = serializers.CharField(max_length=4, min_length=4, required=True, label='图片验证码')

    image_code_id = serializers.UUIDField(label='uuid')

    def validate(self, attrs):

        # 1.得到用户输入的验证码
        text = attrs.get('text')
        image_code_id = attrs.get('image_code_id')
        # 2.获取redis的验证码
        redis_conn = get_redis_connection('code')
        redis_text = redis_conn.get('img_%s'% image_code_id)
        # 2.1 判断是否存在
        if redis_text is None:
            raise serializers.ValidationError('验证码已过期')
        # 2.2 删除
        redis_conn.delete('img_%s'% image_code_id)
        # 3.比较
        # 注意点: redis的数据是bytes类型
        #   转化为小写   .lower()
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError('输入不一致')
        return attrs
