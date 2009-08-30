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
