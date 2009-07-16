from django.conf.urls.defaults import *
from django.contrib.auth.views import *

from gamemasterradio.radio.views import *

import settings

urlpatterns = patterns('gamemasterradio.radio.views',
    (r'^logout/$', 'logout_view'),
    (r'^profile/$', 'index'),
)

urlpatterns += patterns('django.contrib.auth.views',
    (r'^login/$', 'login'),
)

