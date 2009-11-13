from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DATA}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),        
    (r'^', include('metadata.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('profiles.urls')),


)
