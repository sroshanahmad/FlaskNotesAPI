from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate
# from flask_rebar import RequestSchema, ResponseSchema

db = SQLAlchemy()

# class model_name(db.model)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class NoteSchema(Schema):
    id = fields.Int(requied=False)
    data = fields.String(requied=False)
    date = fields.DateTime(requied=False)
