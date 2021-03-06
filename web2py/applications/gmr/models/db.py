# coding: utf8

if False:
    from gluon.sql import *
    from gluon.validators import *

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client())
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## comment/uncomment as needed

from gluon.tools import *
auth=Auth(globals(),db)                      # authentication/authorization
auth.settings.hmac_key='sha512:50646864-d10a-4c9c-a9b8-f2ddea4712bc'
auth.define_tables()                         # creates all needed tables

from gluon.tools import Recaptcha
auth.settings.captcha = Recaptcha(request,'6LftHgoAAAAAAB6Q96ZB4o85btJR56ApGx4NT-ia', '6LftHgoAAAAAACg6sSARkv-0sm8g4mnn8oCjwm9k')


crud=Crud(globals(),db)                      # for CRUD helpers using auth
service=Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc


# crud.settings.auth=auth                      # enforces authorization on crud
# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None
# auth.settings.mailer=mail                    # for user email verification
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
# auth.messages.verify_email = \
#  'Click on the link http://.../user/verify_email/%(key)s to verify your email'
## more options discussed in gluon/tools.py
#########################################################################

#########################################################################
## Define your tables below, for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password',''integer'','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id 'integer' autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('artist',
    Field('user_id',db.auth_user),
    Field('name'),
    Field('description'),
    Field('image', 'upload')
)

db.define_table('track',
    Field('artist_id',db.artist),
    Field('name'),
    Field('description'),
    Field('mp3', 'upload'),
#   PASS
    Field('positivity', 'integer'),
    Field('aggression', 'integer'),
    Field('speed', 'integer'),
    Field('suspense', 'integer')
)

db.define_table('preset',
    Field('name'),
    Field('positivity', 'integer'),
    Field('aggression', 'integer'),
    Field('speed', 'integer'),
    Field('suspense', 'integer'),
    Field('user_id', db.auth_user)
)

db.define_table('playlist',
    Field('name'),
    Field('user_id',db.auth_user)
)

db.define_table('playlist_track',
    Field('playlist_id',db.playlist),
    Field('track_id',db.track),
    Field('position','integer')
)

db.define_table('nudge',
    Field('user_id',db.auth_user),
    Field('track_id',db.track),
    Field('nudgeTime','datetime'),
    Field('pass_attribute','integer'),
    Field('direction')  
)

db.define_table('played',
    Field('user_id',db.auth_user),
    Field('track_id',db.track),
    Field('playedTime','datetime')
)

db.define_table('played_to_end',
    Field('user_id',db.auth_user),
    Field('track_id',db.track),
    Field('finishedTime','datetime')
)

db.define_table('faq',
    Field('question'),
    Field('answer')
)

db.define_table('about',
    Field('title'),
    Field('body'),
    Field('image','upload'),
)
