from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_cors import CORS
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    #initialise app
    app = Flask(__name__) 
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    #print(app.root_path) It points to the directory where your Flask application script (the Python file where you create your Flask app) is located. This is often the file where you write your app = Flask(__name__) line.
    print(app.instance_path) #app.instance_path points to a directory where you can store instance-specific data or configuration files.This directory is typically used for files that should not be part of your version-controlled codebase (like Git), such as configuration files with sensitive information (e.g., secret keys, database connection strings). Flask will create a folder 'instance' for you and this is your instance path
    #It's a good place to store instance-specific data that your Flask app might need to read or write during runtime.
    #In essence, instance-specific data is data or files that are unique to a particular instance of your application to ensure isolation and separation of concerns between different instances, such as development, testing, and production. This helps maintain the integrity and security of each instance and allows for better management and configuration in different environments.'''
    
    # Secret key - secure/encrypt cookies/session data (should be in all flask app?)
    app.config['SECRET_KEY'] = 'fdefefefef' #any random value  

    #telling where db is located or where to look. (this will assume instance path by default)(we are using sqlite) (IGNORE:stores db in this website folder)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    #app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/{DB_NAME}" #if you wanted to have it in /website
    
    # setting app to use database
    db.init_app(app)
    



    #If you define models in other modules, you must import them before calling create_all, otherwise SQLAlchemy will not know about them.
    from .templates.models import Note
    #Checking if database exists, if not create it
    create_db(app)

    from .templates.views import views

    app.register_blueprint(views, url_prefix='/')
    # url prefix tells how to reach to blueprint.
    #let's say I had given as:
    # app.register_blueprint(auth, url_prefix='/home/')
    # and I had defined my auth.route('login')
    #then to access, I have to type /home/login to reach the file
    


    return app
def create_db(app):
   #checking in instance folder
   if not path.exists(f"{app.instance_path}/{DB_NAME}"):
        with app.app_context(): #create_all requires application context
            db.create_all()
            print('Created Database!')
