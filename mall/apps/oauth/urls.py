from django.conf.urls import url
from . import views

urlpatterns = [

    #   /oauth/qq/statues/
    url(r'^qq/statues/$', views.QQ_OauthURLView.as_view(), name='statues'),

    # /oauth/qq/users/
    # url(r'^qq/users/$', views.QQAuthCreateView.as_view())
    url(r'^qq/users/$', views.QQ_TokenView.as_view(), name='qqtoken'),

]