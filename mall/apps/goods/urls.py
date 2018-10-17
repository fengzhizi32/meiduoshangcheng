# coding:utf8
from django.conf.urls import url
from . import views

urlpatterns = [
    #/goods/categories/
    url(r'^categories/$',views.HomeView.as_view(),name='cagegories'),
]