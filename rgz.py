from flask import Blueprint, redirect, request, render_template
from Db import db
from Db.models import users, books
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import string

rgz = Blueprint("rgz", __name__)
books_per_page = 20

@rgz.route("/books")
@login_required
def book():
    my_books = users.query.filter_by(id = current_user.id).all()
    page = int(request.args.get('page', 1))
    offset = (page - 1) * books_per_page
    books_list = books.execute(f"SELECT * FROM books LIMIT {books_per_page} OFFSET {offset}").fetchall()
    show_next_button = books.execute("SELECT COUNT(*) FROM books OFFSET :offset+20 LIMIT 1").fetchone()[0]
    return render_template("books.html", books = my_books, username = current_user.username, books_list = books_list, page=page, show_next_button=show_next_button)

@rgz.route('/next')
def next_books():
    page = int(request.args.get('page', 1)) + 1
    return redirect('book_list', page=page)

@rgz.route('/new_books', methods=['GET', 'POST'])
def new_books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        number_of_pages = request.form['page_count']
        publishing_house = request.form['publisher']
        new_book = books(title=title, author=author, number_of_pages=number_of_pages, publishing_house=publishing_house)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/str')
    return render_template('new_books.html')

@rgz.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = books.query.get(book_id)
    if book is not None:
        db.session.delete(book)
        db.session.commit()
    return redirect('/str')

@rgz.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = books.query.get(book_id)
    if book is not None:
        if request.method == 'POST':
            book.title = request.form['title']
            book.author = request.form['author']
            book.number_of_pages = request.form['page_count']
            book.publishing_house = request.form['publisher']
            db.session.commit()
            return redirect('/str')
        else:
            return render_template('edit.html', book=book)


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
        filtered_books = query.all()
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
    return render_template('books.html', username=username, books=all_books)

