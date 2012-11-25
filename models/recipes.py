from datetime import datetime


db.define_table("Recipes",
    Field('uploadTime', 'datetime', default=datetime.utcnow()),
    Field('title', 'string', length=1000, requires = IS_NOT_EMPTY()),
    Field('description', 'text', requires = IS_NOT_EMPTY()),
    Field('owner', 'reference auth_user', default = auth.user_id),
    Field('rating', 'double', default = 0),
    Field('picture', 'upload', requires = IS_NOT_EMPTY())
    )


db.Recipes.uploadTime.writable = False
db.Recipes.owner.writable = False
