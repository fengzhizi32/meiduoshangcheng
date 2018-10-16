# coding:utf8
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views


urlpatterns = [
    # /users/usernames/(?P<username>\w{5,20})/count/
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.RegisterUserNameView.as_view()),

    # /users/phones/(?P<mobile>1[345789]\d{9})/count/
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$', views.RegisterMoblieView.as_view()),

    # 进行登陆认证,返回token
    #/users/auths/
    url(r'^auths/$', obtain_jwt_token, name='auths'),

    url(r'^infos/$', views.UserCenterInfoView.as_view()),

    url(r'^emails/$', views.UserEmailView.as_view()),

    url(r'^emails/verification/$', views.UserEmailActiveView.as_view()),

    url(r'^addresses/$', views.AddressView.as_view()),

    url(r'^$', views.RegisterCreateUserView.as_view()),


]