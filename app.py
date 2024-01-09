from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy 
from Db import db
from Db.models import user
from flask_login import LoginManager
import psycopg2

from rgz import rgz

app = Flask(__name__)

app.secret_key = "123"
user_db = "admin_knowledge_base_orm"
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "knowledge_base_orm"
password = "123"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "rgz.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

app.register_blueprint(rgz)