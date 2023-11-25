# Blueprint allows us to create urls. helps in knowing that our routes will reside here
from flask import Blueprint,render_template, request, flash, redirect, url_for, jsonify
from website import db
from .models import Note
from flask_cors import cross_origin

views = Blueprint('views', __name__) #telling that our routes are inside here. Helps in differentiation. these to have to be same (views)

#to define route (this is decorator)
@views.route('/notes/', methods = ['GET','POST']) #takes url.(how you want to reach it). We want to definbe it for our homepage
# this function runs whenever we go to this '/' url. (main page of our wesbite)
@cross_origin()
def operationOnSingleNote():
    if request.method=='GET':
        notes = Note.query.all()
        notes_json = [{'id':note.id, 'data':note.data, 'date': note.date } for note in notes]
        return jsonify({'notes':notes_json})
    
    elif request.method=='POST':
        response_data = request.get_json()
        note = Note(data = response_data)
        db.session.add(note)
        db.session.commit()
        return 'Note Created !'
        

@views.route('/notes/<int:id>', methods = ['GET','PUT','DELETE'])
@cross_origin()
def operationsOnNotes(id):

    if request.method=='GET':
        note = Note.query.get_or_404(id)
        note_json = {'id': note.id, 'data': note.data, 'date': note.date}
        return jsonify(note_json)
    
    elif request.method=='PUT':
        
        note = Note.query.get_or_404(id)
        note_content = request.get_json()
        note.data = note_content['data']
        db.session.commit()
        return 'Note Updated !'
        
    
    elif request.method=='DELETE':
        note = Note.query.get_or_404(id)
        db.session.delete(note)
        db.session.commit()
        print('deleted')
        return "Note Deleted !"



    

        