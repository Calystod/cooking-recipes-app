from flask_login import UserMixin, current_user
from main import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250))
    name = db.Column(db.String(250))
    picture = db.Column(db.String(250))
    description = db.Column(db.Text())
