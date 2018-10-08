# coding:utf8
from django.conf.urls import url
from . import views

urlpatterns = [
    # /verifications/imagecodes/(?P<image_code_id>.+)/
    url(r'^imagecodes/(?P<image_code_id>.+)/$', views.RegisterImageCodeView.as_view()),


]