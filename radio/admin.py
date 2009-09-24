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

from django.contrib import admin

from gamemasterradio.radio.models import Track, Feedback

class TrackAdmin(admin.ModelAdmin):
    list_display = ('artist', 'name')           
    search_fields = ['artist', 'name']
    list_filter = ('artist', 'name')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user','url', 'subject','description')           
    search_fields = ['url', 'subject','description']
    list_filter = ('user','url', 'subject','description')  


admin.site.register(Track, TrackAdmin)
admin.site.register(Feedback, FeedbackAdmin)
