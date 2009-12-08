# coding: utf8

import operator

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def getDeviation(track,positivity,aggression,speed,suspense):
    return 1

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

def getTracks():
    
    genreDict = {}
    track_list_sorted = []
    tracks = db().select(db.track.ALL)

    #Add all tracks to a dictionary with the track as the key, deviation as value
    for track in tracks:
        genreDict[getDeviation(track,request.args(0),request.args(1),request.args(2),request.args(3))] = track

    #sort the dictionary by value, convert to a list of tuples
    genreList = sorted(genreDict.keys()) 

    #discard the deviation values to get back to a track list
    for key in genreList:
        track_list_sorted.append(genreDict[key])
      
    return(
        track_list_sorted[0]
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
