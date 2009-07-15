from django.conf.urls.defaults import *
from gamemasterradio.blog.models import Entry
from tagging.views import tagged_object_list

info_dict = {
	'queryset': Entry.objects.filter(status=1),
	'date_field': 'pub_date',
	#'allow_future': True,
}

urlpatterns = patterns('django.views.generic.date_based',
	(r'(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(info_dict, slug_field='slug',template_name='blog/detail.html')),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', dict(info_dict, template_name='blog/list.html')),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$','archive_day',dict(info_dict,template_name='blog/list.html')),
	(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$','archive_month', dict(info_dict, template_name='blog/month_list.html')),
	(r'^(?P<year>\d{4})/$','archive_year', dict(info_dict, template_name='blog/year_list.html', make_object_list=True)),
	(r'^$','archive_index', dict(info_dict, template_name='blog/archive_list.html')),
)

urlpatterns += patterns('gamemasterradio.blog',
    (r'^tags/(?P<slug>[-\w]+)/$', 'tag_views.tag_detail'),
)
