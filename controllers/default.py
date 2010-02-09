# coding: utf8

import operator, datetime

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

@auth.requires_login()
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


@auth.requires_login()
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


@auth.requires_login()
def getArtists():
    """
    Return all artists
    """
    return artistsDict(db().select(db.artist.ALL))

@auth.requires_login()
def artistsDict(artists):
    """
    Creates a dictionary containing the artist [id -> name]
    Input is a list of artist db objects
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


@auth.requires_login()
def jsArtistLookup():
    """
    Ajax method for converting artist ID (int) to artist name (String)
    """
    return artistLookup(int(request.args(0)))


@auth.requires_login()
def artistLookup(id):
    """
    Method for converting artist ID (int) to artist name (String)
    """
    return getArtists()[id]


@auth.requires_login()
def nextTrack():
    """
    Gets the next track object, while simultaniously removing it from the playlist
    """
    if (len(session.currentPlaylist) > 0):
        return dict(
            track = session.currentPlaylist.pop(0),
            end = False
        )
    else:
        return dict(end=True)


@auth.requires_login()
def getPlaylist():
    """
    Returns the current playlist (List of Track objects)
    """
    return session.currentPlaylist


@auth.requires_login()
def queuePlaylist():
    """
    Queues new playlist into session, given PASS query
    """
    session.currentPlaylist = createPlaylist()


@auth.requires_login()
def previewPlaylist():
    """
    Returns a playlist to user, given PASS query, with arists dictionary for looking up
    """
    return dict(
    playlist = createPlaylist(),
    lookupArtist = getArtists()
    )


@auth.requires_login()
def createPlaylist():
    """
    Returns playlist, given PASS query
    """
    #args
    p = request.args(0) #positivity
    a = request.args(1) #aggression
    s = request.args(2) #speed
    s = request.args(3) #suspense
    
    genreDict = {}
    playlist = db().select(db.track.ALL)

    #Add all tracks to a dictionary with the track as the key deviation as value
    for track in playlist:
        genreDict[getDeviation(p,a,s,s,track)] = track

    return sortTracks(genreDict)


@auth.requires_login()
def sortTracks(genreDict):
    """
    Takes a dictionary of deviation:track, sorts it by deviation, and returns the ordered list of tracks
    """
    sortedTrackList = []    
    #sort the dictionary by value, convert to a list of tuples
    sortedGenreDict = sorted(genreDict.keys()) 

    #discard the deviation values to get back a sorted track list
    for key in sortedGenreDict:
        sortedTrackList.append(genreDict[key])
        
    return sortedTrackList


@auth.requires_login()
def createPreset():
    """
    Creates a preset for the currently logged-in user
    """
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
    
    
@auth.requires_login()
def getPresets():
    """
    Returns an alphabetical list of the currently logged-in user's presets
    TODO:make it logged-in user specific
    """
    return(
        dict(presets = db().select(db.preset.ALL,orderby=db.preset.name))
    )


@auth.requires_login()
def updatePlaylist(): #TODO: authenticate this
    """
    Creates new playlist, or updates existing
    p = request.args(0) #positivity
    a = request.args(1) #aggression
    s = request.args(2) #speed
    s = request.args(3) #suspense    
    """
    playlistID = int(request.args(0))
    playlistName = request.args(1) 
    
    trackCount = 0
    for item in request['args']:
        trackCount = trackCount + 1
    trackCount = trackCount - 2
    
    if playlistID==0:
        playlist = db.playlist.insert(
            name = playlistName,
            user_id = auth.user.id
        )
        playlistID = playlist.id
    else:
        playlistID = playlistID
        db(db.playlist_track.playlist_id==playlistID).delete()
    
    dict = {}
    for position in range(trackCount):
        pos = position + 2
        dict[position]=request.args(pos)

    for position in range(trackCount-1):
        playListTrack = db.playlist_track.insert(
            playlist_id = playlistID,
            track_id = dict[position],
            position = position
        )
    return(dict)   

@auth.requires_login()
def getPlaylist(): #TODO: authenticate this
    """
    Returns a list of tracks for a given playlist ID
    """
    playlistID = int(request.args(0))
    query = (db.track.id == db.playlist_track.track_id) &    (db.playlist_track.playlist_id == playlistID)
    
    tracks = db(query).select(db.track.ALL)
    
    return(
        dict(
        tracks = tracks,
        lookupArtist = getArtists()
        )
    )


def deletePreset(): #TODO: authenticate this
    """
    Delete a preset
    """
    presetID = request.args(0)
    db(db.preset.id==presetID).delete()


def deletePlaylist(): #TODO: authenticate this
    """
    Delete a playlist
    """
    playlistID = request.args(0)
    db(db.playlist_track.playlist_id==playlistID).delete()
    db(db.playlist.id==playlistID).delete()


def trackPlayed():
    """
    Logs when a track starts to play, and which user played it
    """
    checkin = db.played.insert(
        track_id=request.vars.track,
        playedTime=datetime.datetime.now(),
        user_id = auth.user.id
    )
    return dict(checkin = checkin)


def trackPlayedToEnd():
    """
    Logs when a track has played all the way through, and which user played it
    """
    checkin = db.played_to_end.insert(
        track_id=request.vars.track,
        playedTime=datetime.datetime.now(),
        user_id = auth.user.id
    )
    return dict(checkin = checkin)

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


@auth.requires_login()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
