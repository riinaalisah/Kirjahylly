from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
from sqlalchemy import text

from application import app, db, login_required
from application.books.models import Book
from application.books.forms import BookForm
from application.authors.models import Author
from application.auth.models import User

import uuid


@app.route("/books/", methods=["GET"])
def books_index():
    user = current_user
    return render_template("books/list.html", books=Book.all_books(), user=user)


@app.route("/books/new/")
@login_required(role="user")
def books_form():
    return render_template("books/new.html", authors=Author.all_authors())


@app.route("/books/", methods=["POST"])
@login_required(role="user")
def books_create():
    form = request.form

    book = Book(name=request.form["inputName"], pages=request.form["inputPages"], isbn=request.form["inputIsbn"])
    authorname = request.form["dropdown"]
    names = authorname.split(" ")
    author = Author.query.filter_by(firstname=names[0], lastname=names[1]).first()

    db.session().add(book)
    author.books.append(book)
    author.books_count = author.books_count + 1
    db.session().commit()

    return redirect(url_for("books_index"))


@app.route("/books/<book_id>/", methods=["POST"])
@login_required(role="user")
def book_add_to_user(book_id):
    book = Book.query.filter_by(id=book_id).first()
    user = User.query.filter_by(username=current_user.username).first()

    if book not in user.mybooks:
        user.mybooks.append(book)
        db.session().commit()
        flash("Kirja lisätty onnistuneesti omaan kirjahyllyyn!", 'success')

    else:
        flash("Kirja on jo lisätty omaan kirjahyllyyn!", 'warning')

    return redirect(url_for("books_index"))


@app.route("/books/info/<bookname>", methods=["GET", "POST"])
@login_required(role="user")
def book_info(bookname):

    book = Book.query.filter_by(name=bookname).first()
    book = Book.book_info(book.id)

    return render_template("books/bookinfo.html", book=book)
