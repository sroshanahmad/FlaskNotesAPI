from flask_cors import cross_origin
from flask_rebar import Rebar, RequestSchema, ResponseSchema
from marshmallow import Schema, fields, validate
from website import db
from .models import Note

rebar = Rebar()
registry = rebar.create_handler_registry(prefix='/api')

class GetNoteResponseSchema(ResponseSchema):
    id = fields.Int(requied=True)
    data = fields.String(requied=True)
    date = fields.DateTime(requied=True)

class PostNoteRequestSchema(RequestSchema):
    data = fields.String(requied=True, validate=validate.Length(min=3))

class PutNoteRequestSchema(RequestSchema):
    id = fields.Int(requied=True)
    data = fields.String(requied=True, validate=validate.Length(min=3))
    date = fields.DateTime(requied=True)

class DeleteNoteRequestSchema(RequestSchema):
    id = fields.Int(requied=True)

@registry.handles( rule='/notes', method='GET', response_body_schema=GetNoteResponseSchema(many=True) )
@cross_origin()
def get_notes():
    """To get all the notes"""
    notes = Note.query.all()
    schema = GetNoteResponseSchema(many=True)
    result = schema.dumps(notes)
    return result

@registry.handles( rule='/notes/<int:id>', method='GET', response_body_schema=GetNoteResponseSchema() )
@cross_origin()
def get_note(id):
    """To get single note based on id"""
    note = Note.query.get_or_404(id)
    schema = GetNoteResponseSchema()
    result = schema.dump(note)
    return result

@registry.handles( rule='/notes', method='POST', request_body_schema=PostNoteRequestSchema(), response_body_schema=None )
@cross_origin()
def create_note():
    """To create a note"""
    user_input = rebar.validated_body # Validated data
    note = Note(data = user_input["data"])
    db.session.add(note)
    db.session.commit()
    return 'Note Created !'


@registry.handles( rule='/notes/<int:id>', method='PUT', request_body_schema=PutNoteRequestSchema(),response_body_schema=None )
@cross_origin()
def update_note(id):
    """To update 'data' in note"""
    user_input = rebar.validated_body
    note = Note.query.get_or_404(id)
    note.data = user_input['data']
    db.session.commit()
    return 'Note Updated !'


@registry.handles( rule='/notes/<int:id>', method='DELETE', response_body_schema=None )
@cross_origin()
def delete_note(id):
    """To delete a note"""
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return "Note Deleted !"



    

        