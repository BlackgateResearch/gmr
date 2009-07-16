from django.conf.urls.defaults import *
from gamemasterradio.radio.views import *
import settings

urlpatterns = patterns('gamemasterradio.radio.views',
    (r'^$', 'index'),
    (r'^radio/playlist.xspf$', 'playlist'),
    (r'^crossdomain.xml$', 'crossdomain'),
)
