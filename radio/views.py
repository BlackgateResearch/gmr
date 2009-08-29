# Change the address from localhost for production
# Previous line unnessisary as of revision 14ish

from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django import http

from gamemasterradio.radio.models import Track, GenreForm

import operator

@login_required
def index(request):
    def errorHandle(error):
        form = RadioForm()
        return render_to_response('radio', {
                                  'error' : error,
                                  'form' : form,
         })
    if request.method == 'POST': # If the form has been submitted...
        form = GenreForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
              speed = request.POST['speed']
              combat = request.POST['combat']
              suspense = request.POST['suspense']
              positive = request.POST['positive']
        return http.HttpResponseRedirect('/radio/listen/' + speed + '-' + combat + '-' + suspense + '-' + positive) # Redirect after POST
    else:
        form = GenreForm() # An unbound form
    
        t = loader.get_template('radio/selectGenre.html')
        c = RequestContext(request, {
            'form': form,
        })  
        return render_to_response("radio/selectGenre.html", c)
   

def logout_view(request):
    logout(request)
    return http.HttpResponseRedirect('/')

@login_required
def listen(request, genre = False):

    '''
    #if (gSpeed) and (gCombat) and (gSuspense) and (gPositive):
    #user has selected genre
    gSpeed = genre.split("-")[0]
    request.session['gSpeed'] = gSpeed
    
    gCombat = genre.split("-")[1]
    request.session['gCombat'] = gCombat
    
    gSuspense = genre.split("-")[2]
    request.session['gSuspense'] = gSuspense
    
    gPositive = genre.split("-")[3]
    request.session['gPositive'] = gPositive

    genreName = gSpeed + "-" + gCombat + "-" + gSuspense + "-" + gPositive
    '''
    
    request.session['genre'] = genre
    t = loader.get_template('radio/listen.html')
    c = RequestContext(request, {
        'genreName' : genre,
    })  
    return render_to_response("radio/listen.html", c)

def playlist(request):
    
    genreDict = {}
    track_list_sorted = []
    
    genre = request.session['genre']
    track_list = Track.objects.all()
    
    gSpeed = genre.split("-")[0]
    gCombat = genre.split("-")[1]
    gSuspense = genre.split("-")[2]
    gPositive = genre.split("-")[3]

    
    #Add all tracks to a dictionary with the track as the key, deviation as value
    for track in track_list:
        genreDict[track] = track.getDeviation(gSpeed,gCombat,gSuspense,gPositive)
        
    #sort the dictionary by value, convert to a list of tuples
    genreList = sorted(genreDict.items(), key=operator.itemgetter(1))

    #discard the deviation values to get back to a track list
    for item in genreList:
        track_list_sorted.append(item[0])
    
    t = loader.get_template('radio/playlist.xml')
    c = Context({
        'track_list': track_list_sorted,
        'genre' : genre
    })    
    return HttpResponse(t.render(c), mimetype='application/xml') 
    
def crossdomain(request):
    t = loader.get_template('radio/crossdomain.xml')
    c = Context({
    })    
    return HttpResponse(t.render(c), mimetype='application/xml')

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact.html', {
        'form': form,
    })


