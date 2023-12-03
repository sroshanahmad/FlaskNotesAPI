from flask import Flask

from os import path
from flask_cors import CORS
from flask_rebar import Rebar
from .templates.views import rebar
from .templates.models import db,Note


DB_NAME = 'database.db'

# rebar = Rebar()
# registry = rebar.create_handler_registry(prefix='/')

def create_app():
    app = Flask(__name__) 
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = 'fdefefefef' #any random value  
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    
    db.init_app(app)
    create_db(app)

    rebar.init_app(app)
    
    CORS(app, resources={r"/notes/*": {"origins": "http://localhost:3000"}})

    return app

def create_db(app):
   #checking in instance folder
   if not path.exists(f"{app.instance_path}/{DB_NAME}"):
        with app.app_context(): #create_all requires application context
            db.create_all()
            print('Created Database!')
