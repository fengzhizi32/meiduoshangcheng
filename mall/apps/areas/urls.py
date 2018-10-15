from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import AreasReadOnlyViewSet

router = DefaultRouter()
router.register(r'infos', AreasReadOnlyViewSet, base_name='areas')

urlpatterns = [
    # url(r'^', include(router.urls)),
]
# 添加 省, 市, 区/县 信息查询路由
urlpatterns += router.urls
