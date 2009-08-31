from django.conf.urls.defaults import *

import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^blog/', include('gamemasterradio.blog.urls')),
    (r'^accounts/', include('gamemasterradio.account.urls')), 
    (r'^radio/', include('gamemasterradio.radio.urls')),
)

urlpatterns += patterns('gamemasterradio.radio.views',
    (r'^$', 'index'),
    (r'^crossdomain.xml$', 'crossdomain'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    )

