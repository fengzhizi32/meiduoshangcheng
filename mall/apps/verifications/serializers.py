# coding:utf8
from rest_framework import serializers

# 序列化器:

class RegisterSmsCodeSerializer(serializers.Serializer):
    """
    数据验证的方法:
    1.字段类型验证
    2.选项验证
    3.单个字段验证
    4.多个字段验证
    """
    # 用户输入的图片验证码
    text = serializers.CharField(max_length=4, min_length=4, required=True, label='图片验证码')

    image_code_id = serializers.UUIDField(label='uuid')

    def validate(self, attrs):

        text = attrs.get('text')
        image_code_id = attrs.get('image_code_id')
