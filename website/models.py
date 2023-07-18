# Create db models
# Need one for users, one for notes
import sys
from os import path
# my python path is a little wonky, you probably won't need this line
sys.path.append(path.dirname(path.abspath(__file__)))
from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    # -------- I had to add this, not in original code. Unsure why, just what the error said
    __table_args__ = {'extend_existing': True}
    # ---------
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default=func.now())
    # All notes must belong to a user. This is the association
    # Use a foriegn key for this
    # These are keys that reference an id in another db table column.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    __tablename__ = 'user' # I just tested this, it is the default name of the table
    # -------- I had to add this, not in original code. Unsure why, just what the error said
    __table_args__ = {'extend_existing': True}
    # ---------
    # for all objects in a db you need a primary key
    # this is used to identify the object
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique= True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

