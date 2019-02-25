from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
from sqlalchemy import text

from application import app, db, login_required
from application.books.models import Book
from application.authors.models import Author
from application.auth.models import User


@app.route("/books/", methods=["GET"])
def books_index():
    user = current_user
    return render_template("books/list.html", books=Book.all_books(), user=user)


@app.route("/books/new/", methods=["GET", "POST"])
@login_required(role="ANY")
def books_new():
    if request.method == "GET":
        return render_template("books/new.html", authors=Author.all_authors())

    else:
        bookname = request.form["inputName"]

        authorname = request.form["dropdown"]
        splitname = authorname.split(" ")
        author = Author.query.filter_by(firstname=splitname[0], lastname=splitname[1]).first()

        authors_books = Author.authors_books_by_author_name(splitname[0], splitname[1])
        for row in authors_books:
            if row[4].lower() == bookname.lower():
                flash("Kyseinen kirja on jo lisätty tietokantaan.", 'warning')
                return render_template("books/new.html", authors=Author.all_authors())

        pages = request.form["inputPages"]
        if pages == "":
            pages = None
        book = Book(name=bookname, pages=pages, isbn=request.form["inputIsbn"])
        db.session().add(book)
        author.books.append(book)
        author.books_count = author.books_count + 1
        db.session().commit()
        flash("Kirja lisätty onnistuneesti!", 'success')
        return redirect(url_for("books_index"))


@app.route("/books/<book_id>/", methods=["POST"])
@login_required(role="ANY")
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
#@login_required(role="ANY")
def book_info(bookname):
    book = Book.query.filter_by(name=bookname).first()
    book = Book.book_info(book.id)

    return render_template("books/bookinfo.html", book=book)


@app.route("/books/delete/<bookname>/<id>/", methods=["GET", "POST"])
@login_required(role='admin')
def admin_delete_book(bookname, id):
    book = Book.book_info(id)

    if request.method == "GET":
        return render_template("books/deletebook.html", book=book)

    else:
        author = Author.query.filter_by(firstname=book.firstname, lastname=book.lastname).first()

        stmt = text("DELETE FROM authors_books WHERE book_id=:id").params(id=id)
        db.engine.execute(stmt)

        stmt2 = text("DELETE FROM users_books WHERE book_id=:id").params(id=id)
        db.engine.execute(stmt2)

        stmt3 = text("DELETE FROM book WHERE name=:bookname AND id=:id") \
            .params(bookname=bookname, id=id)
        db.engine.execute(stmt3)

        author.books_count = author.books_count - 1

        db.session().commit()
        flash("Kirja poistettiin onnistuneesti.", 'success')
        return redirect(url_for('books_index'))
