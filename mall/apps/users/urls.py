# coding:utf8
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views


urlpatterns = [
    # /users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.RegisterUserNameView.as_view()),

    # /users/phones/(?P<mobile>1[345789]\d{9})/count/
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$', views.RegisterMoblieView.as_view()),

    url(r'^$', views.RegisterCreateUserView.as_view()),

    # 进行登陆认证,返回token
    #/users/auths/
    # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
    # .eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InJlbnpoaXFpYW5nIiwiZXhwIjoxNTM5MjQwMzgxLCJlbWFpbCI6IiJ9
    # .vGYaozvlKy98a2RoBJ9TTY2yeN7vZW-0H8f56ZG_xEk
    url(r'^auths/$', obtain_jwt_token, name='auths'),

]