from django.conf.urls.defaults import *
from gamemasterradio.radio.views import *
import settings

urlpatterns = patterns('gamemasterradio.radio.views',
    (r'^$', 'index'),
    (r'^playlist.xspf$', 'playlist'),
    (r'listen/(\d{1}-\d{1}-\d{1}-\d{1})$', 'listen'),
    (r'^crossdomain.xml$', 'crossdomain'),
    
)
