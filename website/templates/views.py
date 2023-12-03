from flask_cors import cross_origin
from flask_rebar import Rebar
from marshmallow import Schema, fields, validate
from .models import db,Note

rebar = Rebar()
registry = rebar.create_handler_registry(prefix='/')

class NoteSchema(Schema):
    id = fields.Int(requied=False)
    data = fields.String(requied=False)
    date = fields.DateTime(requied=False)

@registry.handles( rule='/notes/', method='GET', response_body_schema=NoteSchema(many=True) )
@cross_origin()
def get_notes():
    """To get all the notes"""
    notes = Note.query.all()
    schema = NoteSchema(many=True)
    result = schema.dumps(notes)
    return result

@registry.handles( rule='/notes/<int:id>', method='GET', response_body_schema=NoteSchema() )
@cross_origin()
def get_note(id):
    """To get single note based on id"""
    note = Note.query.get_or_404(id)
    schema = NoteSchema()
    result = schema.dump(note)
    return result

@registry.handles( rule='/notes/', method='POST', request_body_schema=NoteSchema(), response_body_schema=None )
@cross_origin()
def create_note():
    """To create a note"""
    user_input = rebar.validated_body # Validated data
    note = Note(data = user_input["data"])
    db.session.add(note)
    db.session.commit()
    return 'Note Created !'


@registry.handles( rule='/notes/<int:id>', method='PUT', request_body_schema=NoteSchema(),response_body_schema=None )
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
    return "Note Deleted !", 204



    

        