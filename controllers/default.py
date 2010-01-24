# coding: utf8

import operator

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def ensurePositive(val):
    """
    TODO: There must be a better way of doing this!
    >>> ensurePositive(0)
    0
    >>> ensurePositive(1)
    1
    >>> ensurePositive(-1)
    1
    """
    if val < 0:
        return val * -1
    else:
        return val


def getDeviation(positivity,aggression,speed,suspense,track):
    """
    Compare the searched-for parameters with a track, return the deviation
    from the track
    TODO: use the sum of the squares
    """
    deviationSpeed = int(positivity) - int(track.positivity)
    deviationCombat = int(aggression) - int(track.aggression)
    deviationSuspense = int(speed) - int(track.speed)
    deviationPositive = int(suspense) - int(track.suspense)

    deviation = ensurePositive(deviationSpeed) \
        + ensurePositive(deviationCombat) \
        + ensurePositive(deviationSuspense) \
        + ensurePositive(deviationPositive)

    return deviation


def artistsDict(artists):
    """
    Creates a dictionary containing the artist [id -> name]
    Input is an artist db object
    """
    artistDict = {}
    for artist in artists:
        artistDict[artist.id] = artist.name
    return artistDict


@auth.requires_login()
def index():
    """
    Home page for GMR
    """
    response.title = "Game Master Radio"
    response.subtitle = "Music for your worlds"
    return dict(message='Welcome to GMR!')

def echo():
    return request.vars.name

def jsArtistLookup():
    return artistLookup(int(request.args(0)))

def flash():
    return dict(message='flash')

def artistLookup(id):
    artistsDictionary = artistsDict(db().select(db.artist.ALL))
    return artistsDictionary[id]

@auth.requires_login()
def nextTrack():
    if (len(session.currentPlaylist) > 0):
        return dict(
            track = session.currentPlaylist.pop(0),
            end = False
        )
    else:
        return dict(end=True)

@auth.requires_login()
def getPlaylist():
    return returnsession.currentPlaylist

@auth.requires_login()
def getTracks():
    #args
    p = request.args(0) #positivity
    a = request.args(1) #aggression
    s = request.args(2) #speed
    s = request.args(3) #suspense
    
    genreDict = {}
    sortedTrackList = []
    artistsDictionary = {}
    tracks = db().select(db.track.ALL)
    artistsDictionary = artistsDict(db().select(db.artist.ALL))
    
    #Add all tracks to a dictionary with the track as the key, deviation as value
    for track in tracks:
        genreDict[getDeviation(p,a,s,s,track)] = track

    #sort the dictionary by value, convert to a list of tuples
    sortedGenreDict = sorted(genreDict.keys()) 

    #discard the deviation values to get back a sorted track list
    for key in sortedGenreDict:
        sortedTrackList.append(genreDict[key])
    
    session.currentPlaylist = sortedTrackList
    
    return(
        dict(
            sortedTrackList = sortedTrackList,
            artistsDictionary = artistsDictionary
        )
    )

@auth.requires_login()
def createPreset():
    name = request.vars.name
    positivity = request.vars.positivity
    aggression = request.vars.aggression
    speed = request.vars.speed
    suspense = request.vars.suspense
    
    preset = db.preset.insert(
        name=name,
        positivity = positivity,
        aggression = aggression,
        speed = speed,
        suspense = suspense,
        user_id = auth.user.id
    )
    return(dict(preset = preset))
    
def artist():
    return artistsDict(artists = db().select(db.artist.ALL))


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)

#don't think we need this
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
