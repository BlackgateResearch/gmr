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
    return response.download(request, db)
    
    
def about():
    """
    About page
    """
    return dict(about = db().select(db.about.ALL)) 


def faq():
    """
    Frequently asked questions page
    """
    return dict(faqs = db().select(db.faq.ALL))

    
def blog():
    redirect("http://blog.gamemasterradio.com")    

  
def index():
    """
    Home page for GMR
    """
    return dict()
