# coding:utf8
from django.conf.urls import url
from . import views


urlpatterns = [
    # /users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.RegisterUserNameView.as_view()),

    # /users/phones/(?P<mobile>1[345789]\d{9})/count/
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$', views.RegisterMoblieView.as_view()),

    url(r'^$', views.RegisterCreateUserView.as_view()),

]