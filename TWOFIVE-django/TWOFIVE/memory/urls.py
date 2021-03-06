from django.conf.urls import url,include
from django.views import static
from TWOFIVE.settings import MEDIA_ROOT
from . import views

urlpatterns = [
    url(r'^homepage/$', views.homepage,name='homepage'),
    url(r'^login/$', views.login_view,name='login_view'),
    url(r'^login/$',views.register,name='register'),
    url(r'^writing/$',views.writing,name='writing'),
    url(r'^publish/$',views.publish,name='publish'),
    url(r'^browsing/$',views.browsing,name='browsing'),
    url(r'^album/$',views.album,name='album'),
    url(r'^settings/$',views.settings,name='settings'),
    url(r'^ajax_name/$',views.ajax_name,name='ajax_name'),
    url(r'^media/(?P<path>.*)$',static.serve,{'document_root':MEDIA_ROOT,}),
    url(r'^user_setting/$',views.user_setting,name="user_setting"),

    url(r'^addArticle/$',views.addArticle, name="addArticle"),


]