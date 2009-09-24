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
    
def tag_liat(request):
    unslug = slug.replace('-', ' ')
    tag = Tag.objects.get(name=unslug)
    tagged_entries = TaggedItem.objects.get_by_model(Entry, tag)
    t = loader.get_template('tags/list.html')
    c = Context({
        'slug':tag,
        'object_list' : tagged_entries
    })    
    return HttpResponse(t.render(c)) 
