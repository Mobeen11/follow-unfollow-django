from django.conf.urls import patterns, include, url

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Project01.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    # url(r'^twitter/', include('twitter_users.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('follow_unfollow.urls')),
    url(r'', include('facebook_image.urls')),
    url(r'^tinymce/', include('tinymce.urls')),


)
urlpatterns += patterns('', (r'^static(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), )
urlpatterns += patterns('', (r'^media(?P<path>.*)$', 'django.views.media.serve', {'document_root': settings.MEDIA_ROOT}), )
# if settings.DEBUG:
#     urlpatterns += patterns('',
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#         url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.STATIC_ROOT,
#         }),
# )
# if settings.DEBUG:
#     urlpatterns += patterns(
#         '',
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
#             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#     )
# if settings.DEBUG:
#     # static files (images, css, javascript, etc.)
#     urlpatterns += patterns('',
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#         'document_root': settings.MEDIA_ROOT}))