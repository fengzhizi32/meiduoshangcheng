# coding:utf8
from rest_framework import serializers

# 采用 ModelSerializer
# 第一点: 可以自动和创建create方法
# 第二点: 有模型关联
class CreateUserSerializer(serializers.ModelSerializer):



    pass