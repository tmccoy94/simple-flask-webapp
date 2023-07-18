import sys
from os import path
# my python path is a little wonky, you probably won't need this line
sys.path.append(path.dirname(path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisismysecretkeyfornow12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    

    from .views import views
    from .auth import auth

    # prefix is just what you lead with on your URL.
    # default prefix for websites is just "/" which is why that takes you home.
    # You would put something for a subdomain like blog e.g."/blog/"

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create a script to check if we ran the db

    from models import User, Note # ----- I had to change this to models from .models
    # ----- For some reason it was duplicating the imported classes when I didn't
    
    create_database(app)

    # must be after db is created
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # by default looks for primary key, so don't have to define id = id

    return app

def create_database(app):
    db_path = path.join('Website Project', 'website', DB_NAME)
    absolute_db_path = path.abspath(db_path)
    # print(f'Absolute path to the database file: {absolute_db_path}') - just troubleshooting
    if not path.exists(absolute_db_path):   
        # ---- I had to add this in order to get the db to create 
        with app.app_context():
            db.create_all()
        print('Created Database!')
    else:
        print('Database file already exists.') # this is just for troubleshooting

