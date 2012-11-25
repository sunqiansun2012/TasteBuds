# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    if(auth.is_logged_in()):
        userINFO = db.auth_user(auth.user_id)
    else:
        userINFO = 0
    recipes = db().select(db.Recipes.ALL, orderby = ~db.Recipes.rating, limitby = (0, 3))
    places = db().select(db.Restaurants.ALL, orderby = ~db.Restaurants.rating, limitby = (0, 3))
    return dict(userINFO = userINFO, recipes = recipes, places = places)
    
@auth.requires_login()    
def login():
    redirect(URL('index'))
    return dict()
    
def logout():
    auth.logout()
    redirect(URL('index'))
    return dict()
    
def recipe():
    if(auth.is_logged_in()):
        userINFO = db.auth_user(auth.user_id)
    else:
        userINFO = 0
    return dict(userINFO = userINFO)
    
def discover():
    return dict()

def community():
    return dict()

def news():
    return dict() 
    
def addRecipe():
    form = SQLFORM(db.Recipes)
    if form.process().accepted:
        redirect(URL('index'))
    return dict(form=form)
    
def addRestaurant():
    form = SQLFORM(db.Restaurants)
    if form.process().accepted:
        redirect(URL('index'))
    return dict(form=form)
    
def readRecipe():
    recipe = db.Recipes(request.args[0])
    
    return dict(recipe = recipe)   
    
def readRestaurant():
    place = db.Restaurants(request.args[0])
    
    return dict(place = place)          
    
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
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
