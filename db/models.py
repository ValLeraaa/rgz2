from . import db
from flask_login import UserMixin

class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(102), nullable=False)
    role = db.Column(db.String, default='user')


class books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    publishing_house = db.Column(db.String(100), nullable=False)





