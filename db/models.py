from . import db
from flask_login import UserMixin

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(102), nullable=False)

    def __repr__(self):
        return f'id:{self.id}, username:{self.username}'

class books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    cover = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    publishing_house = db.Column(db.String(100), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean)
    likes = db.Column(db.Integer)

    def __repr__(self):
        return f'title:{self.title}, article_text:{self.article_text}, cover:{self.cover}, author:{self.author}, number_of_pages:{self.number_of_pages}, publishing_house:{self.publishing_house}'
