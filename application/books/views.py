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


# add a new book
@app.route("/books/new/", methods=["GET", "POST"])
@login_required(role="ANY")
def books_new():
    if request.method == "GET":
        return render_template("books/new.html", authors=Author.all_authors())

    else:
        bookname = request.form["inputName"]
        year = request.form["inputYear"]
        pages = request.form["inputPages"]
        isbn = request.form["inputIsbn"]
        authorname = request.form["dropdown"]

        # check if any input is invalid (spaces)
        if bookname.isspace() or year.isspace() or pages.isspace() or isbn.isspace():
            flash(
                "Virheellinen syöte (kentät eivät saa sisältää pelkästään välilyöntejä). Ole hyvä ja yritä uudestaan.",
                'warning')
            return render_template("books/new.html", authors=Author.all_authors())

        splitname = authorname.split(" ")
        author = Author.query.filter_by(firstname=splitname[0], lastname=splitname[1]).first()

        # check if the book already in database
        booknamequery = Book.check_if_book_with_name_and_authorid_exists(bookname, author.id)
        if booknamequery > 0:
            flash("Kyseinen kirja on jo lisätty tietokantaan.", 'warning')
            return render_template("books/new.html", authors=Author.all_authors())

        book = Book(name=bookname, year=year, pages=pages, isbn=isbn)
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


@app.route("/books/edit/<bookname>/<id>/", methods=["GET", "POST"])
@login_required(role="ANY")
def admin_edit_book_info(bookname, id):
    book = Book.book_info(id)
    currentauthor = Author.query.filter_by(firstname=book.firstname, lastname=book.lastname).first()

    if request.method == "GET":
        return render_template("books/editinfo.html", book=book, authors=Author.all_authors())

    else:
        bookname = request.form["name"]
        year = request.form["year"]
        pages = request.form["pages"]
        isbn = request.form["isbn"]
        authorname = request.form["dropdown"]

        # check for empty inputs
        if bookname.isspace() or year.isspace() or pages.isspace() or isbn.isspace():
            flash(
                "Virheellinen syöte (kentät eivät saa sisältää pelkästään välilyöntejä). Ole hyvä ja yritä uudestaan.",
                'warning')
            return render_template("books/editinfo.html", book=book, authors=Author.all_authors())

        splitname = authorname.split(" ")
        author = Author.query.filter_by(firstname=splitname[0], lastname=splitname[1]).first()

        authorchanged = False
        namechanged = False

        # check if author has changed
        if book.firstname != author.firstname and book.lastname != author.lastname:
            authorchanged = True

        # check if book name changed
        if bookname != book.name:
            namechanged = True

        # check if book info has changed
        if not namechanged and book.year == year and pages == book.pages and isbn == book.isbn and not authorchanged:
            flash("Et muuttanut tietoja.", 'info')
            return render_template("books/editinfo.html", book=book, authors=Author.all_authors())

        # check if book with same name and author in database IF NAME OR AUTHOR HAS CHANGED
        if namechanged and authorchanged:
            booknamequery = Book.check_if_book_with_name_and_authorid_exists(bookname, author.id)
            if booknamequery > 0:
                flash("Kyseinen kirja on jo lisätty tietokantaan.", 'warning')
                return render_template("books/editinfo.html", book=book, authors=Author.all_authors())

        else:
            stmt = text("UPDATE book SET name=:bookname, year=:year, pages=:pages, isbn=:isbn WHERE id=:bookid") \
                .params(bookname=bookname, year=year, pages=pages, isbn=isbn, bookid=book.id)
            db.engine.execute(stmt)

            if authorchanged:
                currentauthor.books_count = currentauthor.books_count - 1  # reduce previous author's book count
                author.books_count = author.books_count + 1  # add to new author's book count

                updateab = text("UPDATE authors_books SET author_id=:authorid"
                                " WHERE author_id=:currentauthorid AND book_id=:bookid") \
                    .params(authorid=author.id, currentauthorid=currentauthor.id, bookid=book.id)
                db.engine.execute(updateab)

            db.session().commit()
            flash("Kirjan tiedot päivitetiin onnistuneesti!", 'success')
            return redirect(url_for("books_index"))
