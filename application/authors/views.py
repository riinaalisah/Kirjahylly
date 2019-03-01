from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
from gunicorn.config import User
from sqlalchemy import text

from application import app, db, login_required
from application.authors.models import Author
from application.auth.models import User
from application.books.models import Book


@app.route("/authors/", methods=["GET"])
def authors_index():
    authors = Author.all_author_by_bookcount()
    return render_template("authors/list.html", authors=authors, user=current_user)


# add a new author
@app.route("/authors/new", methods=["GET", "POST"])
@login_required(role="ANY")
def authors_new():
    if request.method == "GET":
        return render_template("authors/new.html")

    else:
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        # check if name invalid (only spaces)
        if firstname.isspace() or lastname.isspace():
            flash(
                "Virheellinen syöte (kentät eivät saa sisältää pelkästään välilyöntejä). Ole hyvä ja yritä uudestaan.",
                'warning')
            return render_template("authors/new.html")

        # check for spaces in names
        if (len(firstname.split(" ")) > 1) or (len(lastname.split(" ")) > 1):
            flash("Ole hyvä ja poista välilyönnit kirjailijan etu- tai sukunimestä.", 'warning')
            return render_template("authors/new.html")

        # check if author already in database
        authornamequery = Author.check_if_author_in_database(firstname, lastname)
        if authornamequery > 0:
            flash("Kirjailija on jo lisätty tietokantaan.", 'warning')
            return redirect(url_for('authors_new'))

        else:
            a = Author(firstname, lastname)
            db.session().add(a)
            db.session().commit()
            flash("Kirjailija lisätty onnistuneesti!", 'success')
            return redirect(url_for("authors_index"))


@app.route("/authors/<firstname>/<lastname>/", methods=["GET"])
def author_info(firstname, lastname):
    user = current_user
    author = Author.query.filter_by(firstname=firstname, lastname=lastname).first()

    if user.is_authenticated:
        usersbooks = User.get_users_books(user.id)
        return render_template("authors/authorinfo.html", author=author,
                               books=Author.authors_books_by_author_name(author.firstname, author.lastname),
                               usersbooks=usersbooks)

    else:
        return render_template("authors/authorinfo.html", author=author,
                               books=Author.authors_books_by_author_name(author.firstname, author.lastname))


@app.route("/authors/delete/<firstname>/<lastname>/", methods=["GET", "POST"])
@login_required(role='admin')
def admin_delete_author(firstname, lastname):
    author = Author.query.filter_by(firstname=firstname, lastname=lastname).first()

    if request.method == "GET":
        return render_template("authors/deleteauthor.html", author=author)

    else:
        # change book names
        Author.change_booknames_todelete(author.id)
        # delete authorsbooks connection
        Author.delete_authorsbooks_connection(author.id)
        # delete usersbooks connection for books with changed name
        Book.delete_usersbooks_connection_todelete()
        # delete author
        Author.delete_author(author.firstname, author.lastname)
        # delete books with changed name
        Book.delete_books_todelete()

        flash("Kirjailija poistettiin onnistuneesti.", 'success')
        return redirect(url_for('authors_index'))


# edit author info
@app.route("/authors/<firstname>/<lastname>/edit/", methods=["GET", "POST"])
@login_required(role='ANY')
def author_edit_info(firstname, lastname):
    author = Author.query.filter_by(firstname=firstname, lastname=lastname).first()
    if request.method == "GET":
        return render_template("authors/editinfo.html", author=author)

    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        # check if info has changed
        if firstname == author.firstname and lastname == author.lastname:
            flash("Et muuttanut tietoja.", 'info')
            return render_template("authors/editinfo.html", author=author)

        # check for invalid input (only spaces)
        if firstname.isspace() or lastname.isspace():
            flash(
                "Virheellinen syöte (kentät eivät saa sisältää pelkästään välilyöntejä). Ole hyvä ja yritä uudestaan.",
                'warning')
            return render_template("authors/editinfo.html", author=author)

        # check for spaces in name
        if (len(firstname.split(" ")) > 1) or (len(lastname.split(" ")) > 1):
            flash("Ole hyvä ja poista välilyönnit kirjailijan etu- tai sukunimestä.", 'warning')
            return render_template("authors/editinfo.html", author=author)

        # check if author with the name already in database
        authornamequery = Author.check_if_author_in_database(firstname.upper(), lastname.upper())

        if authornamequery == 0:
            Author.update_authorinfo(firstname, lastname, author.id)
            flash("Kirjailijan tiedot muutettu onnistuneesti!", 'success')
            return redirect(url_for("author_info", firstname=firstname, lastname=lastname))

        else:
            flash("Kyseinen kirjailija on jo lisätty tietokantaan.", 'warning')
            return render_template("authors/editinfo.html", author=author)
