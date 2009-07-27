from django.conf.urls.defaults import *
from gamemasterradio.radio.views import *
import settings

urlpatterns = patterns('gamemasterradio.radio.views',
    (r'^$', 'index'),
    (r'^playlist.xspf$', 'playlist'),
    (r'^(\d{1}-\d{1}-\d{1}-\d{1})$', 'radio'),
    (r'^crossdomain.xml$', 'crossdomain'),
    
)
