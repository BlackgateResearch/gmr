from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django import http

def logout_view(request):
    logout(request)
    return http.HttpResponseRedirect('/')
