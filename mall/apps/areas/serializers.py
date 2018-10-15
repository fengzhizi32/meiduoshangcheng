from rest_framework import serializers
from .models import Area

# 省   的序列化器
class AreaSerializer(serializers.ModelSerializer):
    """行政区划信息序列化器"""
    class Meta:
        model = Area
        fields = ('id', 'name')

# 市    的序列化器
class AreaSerializer_1(serializers.ModelSerializer):
    """行政区划信息序列化器"""
    subs = AreaSerializer(many=True, read_only=True)
    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')