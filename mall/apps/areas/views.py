from django.shortcuts import render

# Create your views here.
# 数据查询:
#  省     select * from tb_areas where parent_id is null
#  市     select * from tb_areas where parent_id=140000
# 区/县   select * from tb_areas where parent_id=140900

# GET   /areas/infos/(?P<pk>\d+)/
# 可以写两个视图   也可以使用视图集
# from rest_framework_extensions.cache.mixins import ListCacheResponseMixin,RetrieveCacheResponseMixin,CacheResponseMixin
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import AreaSerializer, AreaSerializer_1
from .models import Area


class AreasReadOnlyViewSet(ReadOnlyModelViewSet):
    """
    queryset -
        应该用于从此视图返回对象的查询集.通常,您必须设置此属性,或覆盖get_queryset()方法.
        如果要覆盖视图方法,则必须调用get_queryset(),而不是直接访问此属性,
        因为queryset将进行一次评估,并且将为所有后续请求缓存这些结果.
    serializer_class -
        应该用于验证和反序列化输入以及序列化输出的序列化程序类.
        通常,您必须设置此属性,或覆盖该get_serializer_class()方法
    """
    # queryset = Area.objects.filter(parent__isnull=True)
    # 重写方法    可以根据需求  返回不同的查询结果集
    def get_queryset(self):
        if self.action == 'list':
            # 省
            return Area.objects.filter(parent__isnull=True)
            # return Area.objects.filter(parent=None).all()
        else:
            # 市
            return Area.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            # 省
            return AreaSerializer
        else:
            # 市
            return AreaSerializer_1



    # serializer_class = AreaSerializer