from django.conf.urls import include, url
from django.contrib import admin
from Project01 import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^home/$', 'facebook_image.views.home', name='home'),
    url(r'^done/$', 'facebook_image.views.done', name='done'),
    url(r'^logout/$', 'facebook_image.views.logout_view', name='logout'),
    url(r'^test/$', 'facebook_image.views.test', name='test'),
    url(r'^save/$', 'facebook_image.views.save', name='save'),
    url(r'^share/$', 'facebook_image.views.share_post', name='share'),
    url(r'^tweet/$', 'facebook_image.views.tweet', name='tweet'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

