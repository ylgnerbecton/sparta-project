from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from sparta_project.settings import DEBUG

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.autodiscover()
'''
    DJANGO URLS
'''
urlpatterns = [
               url(r'^admin/', include(admin.site.urls)),
               url(r'^sparta/', include('apps.core.urls')),
               url(r'^', include('apps.core.urls')),
               ]

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
]

'''
    MEDIA
'''
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)