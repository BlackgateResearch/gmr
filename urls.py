''''
This file is part of GMR.

    GMR is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GMR is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with GMR.  If not, see <http://www.gnu.org/licenses/>.
'''

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

