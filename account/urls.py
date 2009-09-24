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

