from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [

    url(r'^signup/$', views.register_view, name='register_view'),
    url(r'^$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^all/$', views.all_view, name='all_view'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.profile_view, name='profile_view'),
    url(r'^follow/(?P<username>[\w.@+-]+)/$', views.follow_view, name='follow_view'),
    url(r'^post/new/$', views.newpost_view, name='newpost_view'),
    url(r'^post_list/$', views.postlist_view, name='postlist_view'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^userspost', views.following_userspost_view, name='following_userspost_view'),
    url(r'^followusers/(?P<username>[\w.@+-]+)/$', views.follow_users_view, name='follow_users_view')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)