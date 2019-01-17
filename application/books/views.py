from application import app, db
from flask import redirect, render_template, request, url_for
from application.books.models import Book

@app.route("/books/", methods=["GET"])
def books_index():
    return render_template("books/list.html", books = Book.query.all())

@app.route("/books/new/")
def books_form():
    return render_template("books/new.html")

@app.route("/books/<book_id>/", methods=["POST"])
def books_set_read(book_id):
    b = Book.query.get(book_id)
    b.read = True
    db.session().commit()

    return redirect(url_for("books_index"))

@app.route("/books/", methods=["POST"])
def books_create():
    b = Book(request.form.get("name"))

    db.session().add(b)
    db.session().commit()

    return redirect(url_for("books_index"))
