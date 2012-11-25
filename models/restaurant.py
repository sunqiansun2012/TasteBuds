from datetime import datetime


db.define_table("Restaurants",
    Field('uploadTime', 'datetime', default=datetime.utcnow()),
    Field('name', 'string', length=1000, requires = IS_NOT_EMPTY()),
    Field('location', 'text', requires = IS_NOT_EMPTY()),
    Field('description', 'text', requires = IS_NOT_EMPTY()),
    Field('owner', 'reference auth_user', default = auth.user_id),
    Field('rating', 'double', default = 0),
    Field('picture', 'upload', requires = IS_NOT_EMPTY())
    )


db.Restaurants.uploadTime.writable = False
db.Restaurants.owner.writable = False
