# coding:utf8
from django.conf.urls import url
from . import views
from contents import crons

urlpatterns = [
    #/goods/categories/
    url(r'^categories/$', views.HomeView.as_view(), name='cagegories'),

    url(r'^categories/(?P<category_id>\d+)/hotskus/$', views.HotSKUListView.as_view()),

    url(r'^categories/(?P<category_id>\d+)/skulist/$', views.SKUListView.as_view()),

    # url(r'^dsq/$', crons.generate_static_index_html(), name='dingshiqi'),
]