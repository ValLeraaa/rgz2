from flask import Blueprint, redirect, request, render_template
from Db import db
from Db.models import users, books
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user
import string

rgz = Blueprint("rgz", __name__)

@rgz.route("/check")
def ckeck():
    my_users=users.query.all()
    print(my_users)
    return "result in console!"
'''
@rgz.route('/books')
def book_list():
    books = books.query.all()
    return render_template('book_list.html', books=books)

@rgz.route('/filter_books', methods=['GET', 'POST'])
def filter_books():
    title = request.form.get('title')
    author = request.form.get('author')
    number_of_pages = request.form.get('number_of_pages')
    publishing_house = request.form.get('publishing_house')
'''

@rgz.route("/register", methods=["GET", "POST"])
def register():
    errors ={}
    if request.method == "GET":
        return render_template("register_orm.html")
    username_form = request.form.get("username")
    password_form = request.form.get("password")
    isUserExist = users.query.filter_by(username = username_form).first()
    if isUserExist is not None:
        errors = "Пользователь с таким именем уже существует"
        return render_template("register_orm.html", errors=errors)
    if not (username_form or password_form):
        errors = "Пожалуйста, заполните все поля"
        return render_template("register_orm.html", errors=errors)
    if len(password_form) <= 2:
        errors = "Пароль должен содержать больше 3 и более символов"
        return render_template("register_orm.html", errors=errors)
    hashedPswd = generate_password_hash(password_form, method = "pbkdf2")
    newUser = users(username = username_form, password = hashedPswd)
    db.session.add(newUser)
    db.session.commit()
    return redirect("/rgz/login")

@rgz.route("/login", methods = ["GET", "POST"])
def login():
    errors = {}
    if request.method == "GET":
        return render_template("login_orm.html")
    username_form = request.form.get("username")
    password_form = request.form.get("password")
    my_user = users.query.filter_by(username = username_form).first()
    if not (username_form or password_form):
        errors = "Пожалуйста, заполните все поля"
        return render_template("login_orm.html", errors=errors)
    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember = False)
            return redirect("/books")
        else:
            errors = "Неправильный пароль"
            return render_template("login_orm.html", errors=errors)
    else:
        errors = "Пользователя не существует"
        return render_template("login_orm.html", errors=errors)
    
@rgz.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/glav")

@rgz.route("/glav")
def main():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Anon"
    return render_template('str.html', username=username)