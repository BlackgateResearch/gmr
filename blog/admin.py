from django.contrib import admin

from gamemasterradio.blog.models import Entry

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'status')           
    search_fields = ['title', 'body_html', 'tags']
    list_filter = ('pub_date', 'status')
    prepopulated_fields = {"slug" : ('title',)}
    fieldsets = (
		(None, {'fields': (('title', 'status'), 'body_html', ('pub_date'), 'tags', 'slug')}),
    )

admin.site.register(Entry, EntryAdmin)
