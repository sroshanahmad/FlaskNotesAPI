#importing db from website(using __init__.py)
# if outside, from website import db

from website import db
from sqlalchemy.sql import func

#creating db models
# we will have two: 1.user 2.notes

# class model_name(db.model)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    #using func.now(), it will automatically add current date and we wont need to provide that and we want to store timezone as well
    date = db.Column(db.DateTime(timezone=True), default=func.now())

        

