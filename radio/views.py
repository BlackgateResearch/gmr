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

@login_required
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

from gamemasterradio.radio.models import Feedback
@login_required
def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        #form = ContactForm(request.POST) # A form bound to the POST data

        if True: #form.is_valid(): # All validation rules pass

            
            #Create a new feedback item with data
            newFeedback = Feedback()
            newFeedback.user = request.user
            newFeedback.url = request.POST['url']
            newFeedback.subject = request.POST['subject']
            newFeedback.description = request.POST['description']
            newFeedback.save()
            
            #Validaton passed
            html = "PASS"
            return HttpResponse(html)

        else:
            #Validaton failed
            html = "FAIL"
            return HttpResponse(html)
    else:
        #This is an AJAX view, it should always be sent POST data
        return http.HttpResponseRedirect('/') #bounce that sucker back home

@login_required  
def nudge(request):
    if request.method == 'POST': # If the form has been submitted...

        if True: #form.is_valid(): # All validation rules pass


            #grab vars from request
            trackID = request.POST['id']
            genreVar = request.POST['genreVar']
            up = request.POST['up']
            
            #Tweak current track
            track = Track.objects.get(id__exact=trackID) # <- TODO ID goes here!
            
            returnGenreValue = "FAIL" #TODO: we should replace this with a check to see if the variable is initialised before the return
            # TODO I bet there's a better way of doing this...
            if genreVar == "gSpeed":  
                if up == "True":
                    if track.gSpeed < 9:
                        track.gSpeed = track.gSpeed + 1
                        returnGenreValue = track.gSpeed
                elif track.gSpeed > 0:
                    track.gSpeed = track.gSpeed - 1
                    returnGenreValue = track.gSpeed
                
            elif genreVar == "gCombat":
                if up == "True":
                    if track.gCombat < 9:
                        track.gCombat = track.gCombat + 1
                        returnGenreValue = track.gCombat
                elif track.gCombat > 0:
                    track.gCombat = track.gCombat - 1
                    returnGenreValue = track.gCombat
                
            elif genreVar == "gSuspense": 
                if up == "True":
                    if track.gSuspense < 9:
                        track.gSuspense = track.gSuspense + 1
                        returnGenreValue = track.gSuspense
                elif track.gSuspense > 0:
                    track.gSuspense = track.gSuspense - 1
                    returnGenreValue = track.gSuspense
                
            elif genreVar == "gPositive": 
                if up == "True":
                    if track.gPositive < 9:
                        track.gPositive = track.gPositive + 1
                        returnGenreValue = track.gPositive
                elif track.gPositive > 0:
                    track.gPositive = track.gPositive - 1
                    returnGenreValue = track.gPositive
                 
            else: # bad data, bounce those suckers
                return HttpResponse(returnGenreValue)
            
            #Validaton passed
            track.save()
            return HttpResponse(returnGenreValue)

        else:
            #Validaton failed
            return HttpResponse(returnGenreValue)
    else:
        #This is an AJAX view, it should always be sent POST data
        return http.HttpResponseRedirect('/') #bounce that sucker back home
      
@login_required  
def track(request,trackID):
    
    try:
        track = Track.objects.get(id=trackID)
        
        #TODO: There's a lot of ifs here, there's probably a more elegant solution
        if track.gSpeed == 0:
            speedIsMin = True
        else:
            speedIsMin = False
        
        if track.gSpeed == 9:
            speedIsMax = True
        else:
            speedIsMax = False
        
        if track.gCombat == 0:
            combatIsMin = True
        else:
            combatIsMin = False
            
        if track.gCombat == 9:
            combatIsMax = True
        else:
            combatIsMax = False
        
        if track.gSuspense == 0:
            suspenseIsMin = True
        else:
            suspenseIsMin = False
            
        if track.gSuspense == 9:
            suspenseIsMax = True
        else:
            suspenseIsMax = False
        
        if track.gPositive == 0:
            positiveIsMin = True
        else:
            positiveIsMin = False
            
        if track.gPositive == 9:
            positiveIsMax = True
        else:
            positiveIsMax = False
                        
    except:
        return http.HttpResponseNotFound('Track not found!')
    c = RequestContext(request, {
        'track' : track,
        'speedIsMin' : speedIsMin,
        'speedIsMax' : speedIsMax,
        'combatIsMin' : combatIsMin,
        'combatIsMax' : combatIsMax,
        'suspenseIsMin' : suspenseIsMin,
        'suspenseIsMax' : suspenseIsMax,
        'positiveIsMin' : positiveIsMin,
        'positiveIsMax' : positiveIsMax
    })  
    return render_to_response("radio/track.html", c)
