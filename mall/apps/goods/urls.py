# coding:utf8
from django.conf.urls import url
from . import views
from contents import crons

urlpatterns = [

    #/goods/categories/
    url(r'^categories/$', views.HomeView.as_view(), name='cagegories'),

    url(r'^categories/(?P<category_id>\d+)/hotskus/$', views.HotSKUListView.as_view()),

    url(r'^categories/(?P<category_id>\d+)/skus/$', views.SKUListView.as_view()),

]


from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('search', views.SKUSearchViewSet, base_name='skus_search')

urlpatterns += router.urls