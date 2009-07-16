# Change the address from localhost for production
# Previous line unnessisary as of revision 14ish

from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django import http

from gamemasterradio.radio.models import Track, Genre


def index(request):
    t = loader.get_template('radio/index.html')
    #c = Context()  
    c = RequestContext(request)  
    return HttpResponse(t.render(c))

def logout_view(request):
    logout(request)
    return http.HttpResponseRedirect('/')


@login_required
def radio(request, genre="None"):
    if (genre != "None"):
        request.session['genre'] = genre
        genreName = Genre.objects.get(id=genre)
        #user has selected genre 
        t = loader.get_template('radio/radio.html')
        c = RequestContext(request, {
            'genreName' : genreName,
            'genre' : genre
        })  
        return render_to_response("radio/radio.html", c)  
        #return HttpResponse(t.render(c))
    else:
        #user has yet to select genre
        genre_list = Genre.objects.all()
        t = loader.get_template('radio/select.html')
        c = RequestContext(request, {
        'genre' : genre,
        'genre_list' : genre_list
        })    
        return render_to_response("radio/select.html", c) 


def playlist(request):
    #track_list = ['http://namtao.com/gmr/travel-demo.mp3','http://namtao.com/gmr/travel-demo.mp3']
    
    #track_list = Track.objects.all()
    genre = request.session['genre']
    track_list = Track.objects.filter(genre__id=genre)
    t = loader.get_template('radio/playlist.xml')
    c = Context({
        'track_list': track_list,
        'genre' : genre
    })    
    return HttpResponse(t.render(c), mimetype='application/xml') 
    
def crossdomain(request):
    t = loader.get_template('radio/crossdomain.xml')
    c = Context({
    })    
    return HttpResponse(t.render(c), mimetype='application/xml')
   
'''
@login_required
def authtest(request):
    message = "ok"
    t = loader.get_template('test.html')
    c = Context({
        'message': message,
    })    
    return HttpResponse(t.render(c))
'''