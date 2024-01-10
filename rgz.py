from flask import Blueprint, redirect, request, render_template
from Db import db
from Db.models import users, books
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import string

rgz = Blueprint("rgz", __name__)

@rgz.route("/books")
@login_required
def book():
    my_books = users.query.filter_by(id = current_user.id).all()
    return render_template("books.html", books = my_books, username = current_user.username)

@rgz.route('/new_books', methods=['GET', 'POST'])
def new_books():
    if request.method == 'POST':
        title = request.form['title']
 # Сохранение файла и получение пути
        author = request.form['author']
        number_of_pages = request.form['page_count']
        publishing_house = request.form['publisher']

        new_book = books(title=title, author=author, number_of_pages=number_of_pages, publishing_house=publishing_house)
        db.session.add(new_book)
        db.session.commit()

        return redirect('/str')
    return render_template('new_books.html')

@rgz.route('/delete_books', methods=['POST'])
def delete_books(books_id):
    # здесь будет код для отображения деталей книги по её ID
    return render_template('books.html', book_id=books_id)

@rgz.route('/edit_books', methods=['GET', 'POST'])
def edit_books(book_id):
    # Проверяем, что пользователь аутентифицирован и является администратором
        if request.method == 'GET':
            # Здесь будет код для отображения формы редактирования книги по её ID
            return render_template('edit_books.html')
        elif request.method == 'POST':
            # Здесь будет код для обработки изменений в книге
            # Например, обновление информации о книге в базе данных
            return redirect('/str')  # перенаправляем на страницу с деталями книги

@rgz.route('/filter_books', methods=['GET', 'POST'])
def filter_books():
    if request.method == "GET":
        return render_template("filtered_books.html")
    else:
        title = request.form["title"]
        author = request.form['author']
        number_of_pages = request.form['number_of_pages']
        publishing_house = request.form['publishing_house']
        query = books.query
        if title:
            query = query.filter(books.title.ilike(title))
        if author:
            query = query.filter(books.author.ilike(author))
        if number_of_pages:
            query = query.filter(books.number_of_pages == int(number_of_pages))
        if publishing_house:
            query = query.filter(books.publishing_house.ilike(publishing_house))
        filtered_books = query.all()  # Получаем отфильтрованные книги
        return render_template('filtered_books.html', books=filtered_books)
    
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
    if len(password_form) <= 3:
        errors = "Пароль должен содержать больше 3 и более символов"
        return render_template("register_orm.html", errors=errors)
    hashedPswd = generate_password_hash(password_form, method = "pbkdf2")
    newUser = users(username = username_form, password = hashedPswd)
    db.session.add(newUser)
    db.session.commit()
    return redirect("/login")

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
        if my_user.password == password_form:
            login_user(my_user, remember = False)
            return redirect("/str")
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember = False)
            return redirect("/str")
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
    return redirect("/str")


@rgz.route("/str")
def main():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Anon"
    all_books = books.query.all()
    # Передаем книги в шаблон и отображаем их
    return render_template('books.html', username=username, books=all_books)

