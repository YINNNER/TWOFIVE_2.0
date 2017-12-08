# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views import static
from TWOFIVE.settings import MEDIA_ROOT
from . import views

urlpatterns = [
    url(r'^homepage/$', views.homepage,name='homepage'), # 主頁url
    url(r'^login/$', views.login_view,name='login_view'), # 登錄的處理url
    url(r'^login/$',views.register,name='register'),# 注冊的處理url
    url(r'^writing/$',views.writing,name='writing'), # 寫文章界面
    url(r'^publish/$',views.publish,name='publish'), # 發佈按鈕的url
    url(r'^browsing/$',views.browsing,name='browsing'), # 推薦界面的url
    url(r'^album/$',views.album,name='album'), # 相冊界面的url
    url(r'^settings/$',views.settings,name='settings'), # 設置界面的url
    url(r'^media/(?P<path>.*)$',static.serve,{'document_root':MEDIA_ROOT,}),
    url(r'^user_setting/$',views.user_setting,name="user_setting"), # 設置的處理url
]