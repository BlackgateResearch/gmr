from django.views.generic.list_detail import object_detail
from tagging.models import Tag,TaggedItem
from blog.models import Entry

from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django import http

'''
def tag_detail(request, slug):
	unslug = slug.replace('-', ' ')
	tag = Tag.objects.get(name=unslug)
	qs = TaggedItem.objects.get_by_model(Entry, tag)
	return object_list(request, queryset=qs, extra_context={'tag':slug}, template_name='tags/list.html') #detail.html
'''

def tag_detail(request, slug):
    unslug = slug.replace('-', ' ')
    tag = Tag.objects.get(name=unslug)
    tagged_entries = TaggedItem.objects.get_by_model(Entry, tag)
    t = loader.get_template('tags/list.html')
    c = Context({
        'slug':tag,
        'object_list' : tagged_entries
    })    
    return HttpResponse(t.render(c)) 
