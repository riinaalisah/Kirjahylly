from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.books.models import Book
from application.books.forms import BookForm
from application.authors.models import Author
from application.authors.forms import AuthorForm

@app.route("/books/", methods=["GET"])
def books_index():
    return render_template("books/list.html", books = Book.query.all())

@app.route("/books/new/")
@login_required
def books_form():
    return render_template("books/new.html", form = BookForm())

@app.route("/books/<book_id>/", methods=["POST"])
@login_required
def books_set_read(book_id):

    b = Book.query.get(book_id)
    b.read = True
    db.session().commit()

    return redirect(url_for("books_index"))

@app.route("/books/", methods=["POST"])
@login_required
def books_create():
    form = BookForm(request.form)
#    authorform = AuthorForm(request.form)

    if not form.validate():
        return render_template("books/new.html", form = form)

    b = Book(form.name.data)
    a = Author.query.filter_by(firstname=form.author_firstname.data).first()

#    db.session().add(a)

    b.read = form.read.data
    b.account_id = current_user.id
    b.author_id = a.id

 #   a = Author(authorform.firstname.data, authorform.lastname.data)

  #  ab = authors_books(bookform.id.data, authorform.id.data)

    db.session().add(b)
    db.session().commit()

    return redirect(url_for("books_index"))

