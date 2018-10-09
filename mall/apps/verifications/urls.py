# coding:utf8
from django.conf.urls import url
from . import views

urlpatterns = [
    # /verifications/imagecodes/(?P<image_code_id>.+)/
    url(r'^imagecodes/(?P<image_code_id>.+)/$', views.RegisterImageCodeView.as_view()),

    # GET /verifications/smscodes/(?P<mobile>1[345789]\d{9})/?text=xxxx & image_code_id=xxxx
    url(r'^smscodes/(?P<mobile>1[345789]\d{9})/$', views.RegisterSmsCodeView.as_view()),
]