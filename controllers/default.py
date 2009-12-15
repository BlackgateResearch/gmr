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
    >>> ensurePositive(-45)
    45
    >>> ensurePositive(54)
    54
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
    "generates rss feed form the wiki pages"
    import gluon.contrib.markdown as md
    tracks = db().select(db.track.ALL)
    return dict(
        title = 'mywiki rss feed',
        link = 'http://127.0.0.1:8000/mywiki/default/index',
        description = 'mywiki news',
        created_on = request.now,
        items = [
            dict(title = track.name,
            description = track.description,
            ) for track in tracks]
        )

@auth.requires_login()
def getTracks():

    genreDict = {}
    sortedTrackList = []
    artistsDictionary = {}
    tracks = db().select(db.track.ALL)
    artists = db().select(db.artist.ALL)
    artistsDictionary = artistsDict(artists)

    p = request.args(0) #positivity
    a = request.args(1) #aggression
    s = request.args(2) #speed
    s = request.args(3) #suspense
    
    #Add all tracks to a dictionary with the track as the key, deviation as value
    for track in tracks:
        genreDict[getDeviation(p,a,s,s,track)] = track

    #sort the dictionary by value, convert to a list of tuples
    sortedGenreDict = sorted(genreDict.keys()) 

    #discard the deviation values to get back a sorted track list
    for key in sortedGenreDict:
        sortedTrackList.append(genreDict[key])

    return(
        dict(
            sortedTrackList = sortedTrackList,
            artistsDictionary = artistsDictionary
        )
    )

def artist():
    if request.args(0) != None:
        return(request.args(0))

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


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
