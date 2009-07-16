from django.contrib import admin

from gamemasterradio.radio.models import Track

class TrackAdmin(admin.ModelAdmin):
    list_display = ('artist', 'name')           
    search_fields = ['artist', 'name']
    list_filter = ('artist', 'name')


admin.site.register(Track, TrackAdmin)
