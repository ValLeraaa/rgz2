from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager

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

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/menu")
def menu():
    return """
<!doctype html>
<html>
    <head>
        <title>Книги</title>
    </head>
    <body>
        <header>
        НГТУ, ФБ, Расчетно-графическая работа
        </header>

        <h1>Книги</h1>

        <footer>
            &copy; Пахомова Валерия, ФБИ-11, 3 курс, 2023
        </footer>
    </body>
</html>
"""
