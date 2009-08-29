# Change the address from localhost for production
# Previous line unnessisary as of revision 14ish

from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django import http

from gamemasterradio.radio.models import Track

import operator

def index(request):
    t = loader.get_template('radio/select.html') 
    c = RequestContext(request)     
    return HttpResponse(t.render(c))

def logout_view(request):
    logout(request)
    return http.HttpResponseRedirect('/')

@login_required
def radio(request, genre = False):

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
    t = loader.get_template('radio/radio.html')
    c = RequestContext(request, {
        'genreName' : genre,
    })  
    return render_to_response("radio/radio.html", c)  


def playlist(request):
    #track_list = ['http://namtao.com/gmr/travel-demo.mp3','http://namtao.com/gmr/travel-demo.mp3']
    
    #track_list = Track.objects.all()
    genre = request.session['genre']
    track_list = Track.objects.all()
    
    gSpeed = genre.split("-")[0]
    gCombat = genre.split("-")[1]
    gSuspense = genre.split("-")[2]
    gPositive = genre.split("-")[3]
    
    genreDict = {}
    
    #Add all tracks to a dictionary with the track as the key, deviation as value
    for track in track_list:
        genreDict[track] = track.getDeviation(gSpeed,gCombat,gSuspense,gPositive)
        
    #sort the dictionary by value, convert to a list of tuples
    genreList = sorted(genreDict.items(), key=operator.itemgetter(1))
    
    track_list_sorted = []

    #strip
    for item in genreList:
        track_list_sorted.append(item[0])
    
    '''
    li=[[2,6],[1,3],[5,4]]
    li.sort(lambda x, y: cmp(x[1],y[1]))
    print li; # prints [[1, 3], [5, 4], [2, 6]]
    '''
    
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

def radio(request):
    def errorHandle(error):
		    form = RadioForm()
		    return render_to_response('radio', {
				                          'error' : error,
				                          'form' : form,
		     })
    if request.method == 'POST': # If the form has been submitted...
        form = RadioForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
			        speed = request.POST['speed']
			        combat = request.POST['combat']
			        suspense = request.POST['suspense']
			        positive = request.POST['positive']
        return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = RadioForm() # An unbound form

    return render_to_response('radio', {
        'form': form,
    })

