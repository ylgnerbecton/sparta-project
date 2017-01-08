from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.decorators import login_required

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.autodiscover()
'''
    DJANGO URLS
'''
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sparta/', include('apps.urls')),
    url(r'^', include('apps.urls')),
)

'''
    MEDIA
'''
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)