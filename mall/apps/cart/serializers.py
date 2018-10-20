from rest_framework import serializers
from goods.models import SKU


class CartSerializer(serializers.Serializer):

    sku_id = serializers.IntegerField(label='sku_id', required=True, min_value=1)
    count = serializers.IntegerField(label='数量', required=True, min_value=1)
    selected = serializers.BooleanField(label='是否勾选', required=False, default=True)

    def validate(self, attrs):

        # 判断商品是否存在
        sku_id = attrs['sku_id']
        try:
            sku = SKU.objects.get(pk = sku_id)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        # 判断库存是否充足
        count = attrs['count']
        if sku.stock < count:
            raise serializers.ValidationError('库存不足')

        return attrs