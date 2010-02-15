# coding: utf8

import operator

@auth.requires_membership('Artist')
def index():
    """
    Artist's page for GMR
    """
    response.title = "Game Master Radio - artist section"
    response.subtitle = "Music for your worlds"
    return dict(
        artist = db(db.artist.user_id==auth.user.id).select()[0],
        tracks = db(db.track.id == db.artist.id).select()
    )

@auth.requires_login()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)
