from django.conf.urls import url
from oauth import views

urlpatterns = [

    #   /oauth/qq/statues/
    url(r'^qq/statues/$', views.QQAuthURLView.as_view(), name='statues'),

    # /oauth/qq/users/
    url(r'^qq/users/$', views.QQTokenView.as_view(), name='qqtoken'),
]