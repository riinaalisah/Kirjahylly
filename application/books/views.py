from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import text

from application import app, db
from application.books.models import Book
from application.books.forms import BookForm
from application.authors.models import Author
from application.auth.models import User


@app.route("/books/", methods=["GET"])
def books_index():
    user = current_user
    stmt = text("select book_id, author_id, name, firstname, lastname from authors_books join book on "
                "book.id=authors_books.book_id join author on author.id=authors_books.author_id")
    books = db.engine.execute(stmt)

    return render_template("books/list.html", books=books, user=user)


@app.route("/books/new/")
@login_required
def books_form():
    stmt = text("SELECT * FROM author")
    authors = db.engine.execute(stmt)

    return render_template("books/new.html", form=BookForm(), authors=authors)


@app.route("/books/", methods=["POST"])
@login_required
def books_create():
    form = BookForm(request.form)

    if not form.validate():
        return render_template("books/new.html", form=form)

    book = Book(form.name.data)
    authorname = request.form.get("dropdown")
    names = authorname.split(" ")
    author = Author.query.filter_by(firstname=names[0], lastname=names[1]).first()

    db.session().add(book)
    author.books.append(book)
    db.session().commit()

    return redirect(url_for("books_index"))


@app.route("/books/<book_id>/", methods=["POST"])
@login_required
def book_add_to_user(book_id):
    book = Book.query.filter_by(id=book_id).first()
    user = User.query.filter_by(username=current_user.username).first()

    #stmt = text("SELECT book_id FROM users_books WHERE user_id = :userid").params(userid=current_user.id)
    #book_ids = db.engine.execute(stmt)
    #print(book_ids)

    if book not in user.mybooks:
        user.mybooks.append(book)
        db.session().commit()
        flash("Kirja lisätty onnistuneesti omaan kirjahyllyyn!")

    else:
        flash("Kirja on jo lisätty omaan kirjahyllyyn!")

    return redirect(url_for("books_index"))
