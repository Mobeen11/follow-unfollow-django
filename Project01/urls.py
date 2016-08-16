from django.conf.urls import patterns, include, url

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Project01.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('follow_unfollow.urls')),
    url(r'^tinymce/', include('tinymce.urls')),


)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
