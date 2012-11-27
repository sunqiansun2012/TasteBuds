from datetime import datetime
    

    
db.define_table("comments",
    Field('comment', 'text'),
    Field('belongTo', 'reference Recipes'),
    Field('commentor', 'string', length = 1000),
    Field('rateDate', 'datetime')
)
