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
    recipeList = db(db.Recipes.owner == auth.user_id).select()    
    recipes = db().select(db.Recipes.ALL, orderby = ~db.Recipes.rating)
    return dict(userINFO = userINFO, recipeList = recipeList, recipes = recipes)
    
def discover():
    if(auth.is_logged_in()):
        userINFO = db.auth_user(auth.user_id)
    else:
        userINFO = 0
    placeList = db(db.Restaurants.owner == auth.user_id).select()
    places = db().select(db.Restaurants.ALL, orderby = ~db.Restaurants.rating)
    return dict(userINFO = userINFO, placeList = placeList, places = places)

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
    session.currentRecipe = request.args[0]
    rateForm = FORM('Rate or Comment this recipe?',
                     INPUT(_type = 'submit', _value = 'Rate and Comment')
                )
    commentList = db(db.comments.belongTo == session.currentRecipe).select()      
    if rateForm.process().accepted:
        session.title = recipe.title
        session.owner = recipe.owner.first_name + " " + recipe.owner.last_name
        redirect(URL('rateRecipe'))
    return dict(recipe = recipe, rateForm = rateForm, commentList = commentList)   
    
def readRestaurant():
    place = db.Restaurants(request.args[0])
    session.currentRestaurant = request.args[0]
    rateForm = FORM('Rate or Comment this restaurant?',
                     INPUT(_type = 'submit', _value = 'Rate and Comment')
                )
    commentList = db(db.rcomments.belongTo == session.currentRestaurant).select()            
    if rateForm.process().accepted:
        session.title = place.name
        session.owner = place.owner.first_name + " " +place.owner.last_name
        redirect(URL('rateRestaurant'))
    return dict(place = place, rateForm = rateForm, commentList = commentList)
    
@auth.requires_login()        
def rateRecipe():
    form = FORM(
                'Select to Rate',
                 SELECT('bad', 'good', 'very good', 'excellent', _name = 'rating'),
                 BR(),BR(),
                 
                 'your comment: ', TEXTAREA(_name = 'commentText', requires = IS_NOT_EMPTY()),
                 BR(),BR(),
                 
                 INPUT(_type = 'submit', _value = 'Go submit'),
                 A("Cancel", _href = URL("readRecipe", args = [session.currentRecipe]), )
                )
    
    if form.process().accepted:
        recipe = db.Recipes(session.currentRecipe)
        currentRating = recipe.rating
        if form.vars.rating == 'bad':
            currentRating -= 1
        if form.vars.rating == 'good':
            currentRating += 1
        if form.vars.rating == 'very good':
            currentRating += 2         
        if form.vars.rating == 'excellent':
            currentRating += 3 
                
        userINFO = db.auth_user(auth.user_id)
        db.comments.insert(comment = form.vars.commentText, belongTo = session.currentRecipe, commentor = userINFO.first_name + ' ' + userINFO.last_name, rateDate = datetime.utcnow())    
                    
        db(db.Recipes.id == session.currentRecipe).validate_and_update(rating = currentRating)
        db.commit()
        
        redirect(URL('readRecipe', args = [session.currentRecipe]))
              
                
    return dict(form = form)                    

@auth.requires_login()                        
def rateRestaurant():
    form = FORM(
                'Select to Rate',
                 SELECT('bad', 'good', 'very good', 'excellent', _name = 'rating'),
                 BR(),BR(),
                 
                 'your comment: ', TEXTAREA(_name = 'commentText', requires = IS_NOT_EMPTY()),
                 BR(),BR(),
                 
                 INPUT(_type = 'submit', _value = 'Go submit'),
                 A("Cancel", _href = URL("readRestaurant", args = [session.currentRestaurant]), )
                )
    
    if form.process().accepted:
        place = db.Restaurants(session.currentRestaurant)
        currentRating = place.rating
        if form.vars.rating == 'bad':
            currentRating -= 1
        if form.vars.rating == 'good':
            currentRating += 1
        if form.vars.rating == 'very good':
            currentRating += 2         
        if form.vars.rating == 'excellent':
            currentRating += 3 
                
        userINFO = db.auth_user(auth.user_id)
        db.rcomments.insert(comment = form.vars.commentText, belongTo = session.currentRestaurant, commentor = userINFO.first_name + ' ' + userINFO.last_name, rateDate = datetime.utcnow())    
                    
        db(db.Restaurants.id == session.currentRestaurant).validate_and_update(rating = currentRating)
        db.commit()
        
        redirect(URL('readRestaurant', args = [session.currentRestaurant]))
    return dict(form = form)
    
    
def deleteRecipe():
    db(db.Recipes.id == request.args[0]).delete()
    db.commit()
    redirect(URL("recipe"))
    return dict()    
    
def deleteRestaurant():
    db(db.Restaurants.id == request.args[0]).delete()
    db.commit()
    redirect(URL("discover"))
    return dict()     
                
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
