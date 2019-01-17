from flask import redirect, render_template, request, url_for

from application import app, db
from application.books.models import Book
from application.books.forms import BookForm

@app.route("/books/", methods=["GET"])
def books_index():
    return render_template("books/list.html", books = Book.query.all())

@app.route("/books/new/")
def books_form():
    return render_template("books/new.html", form = BookForm())

@app.route("/books/<book_id>/", methods=["POST"])
def books_set_read(book_id):

    b = Book.query.get(book_id)
    b.read = True
    db.session().commit()

    return redirect(url_for("books_index"))

@app.route("/books/", methods=["POST"])
def books_create():
    form = BookForm(request.form)

    if not form.validate():
        return render_template("books/new.html", form = form)

    b = Book(form.name.data)
    b.read = form.read.data

    db.session().add(b)
    db.session().commit()

    return redirect(url_for("books_index"))
