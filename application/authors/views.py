from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
from gunicorn.config import User
from sqlalchemy import text

from application import app, db, login_required
from application.authors.models import Author
from application.auth.models import User


@app.route("/authors/", methods=["GET"])
def authors_index():
    stmt = text("SELECT * FROM author ORDER BY books_count DESC")
    authors = db.engine.execute(stmt)
    return render_template("authors/list.html", authors=authors, user=current_user)

# add a new author
@app.route("/authors/new", methods=["GET", "POST"])
@login_required(role="ANY")
def authors_create():
    if request.method == "GET":
        return render_template("authors/new.html")

    else:
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        # check if name invalid (only spaces)
        if firstname.isspace() or lastname.isspace():
            flash("Virheellinen syöte (kentät eivät saa sisältää pelkästään välilyöntejä). Ole hyvä ja yritä uudestaan.", 'warning')
            return render_template("authors/new.html")

        # check for spaces in names
        if (len(firstname.split(" ")) > 1) or (len(lastname.split(" ")) > 1):
            flash("Ole hyvä ja poista välilyönnit kirjailijan etu- tai sukunimestä.", 'warning')
            return render_template("authors/new.html")

        # check if author already in database
        authornamequery = Author.check_if_author_in_database(firstname, lastname)
        if authornamequery > 0:
            flash("Kirjailija on jo lisätty tietokantaan.", 'warning')
            return redirect(url_for('authors_create'))

        else:
            a = Author(firstname, lastname)
            db.session().add(a)
            db.session().commit()
            flash("Kirjailija lisätty onnistuneesti!", 'success')
            return redirect(url_for("authors_index"))


@app.route("/authors/delete/<firstname>/<lastname>/", methods=["GET", "POST"])
@login_required(role='admin')
def admin_delete_author(firstname, lastname):
    author = Author.query.filter_by(firstname=firstname, lastname=lastname).first()

    if request.method == "GET":
        return render_template("authors/deleteauthor.html", author=author)

    else:
        stmt = text("DELETE FROM authors_books WHERE author_id=:authorid").params(authorid=author.id)
        db.engine.execute(stmt)
        stmt2 = text("DELETE FROM author WHERE firstname=:firstname AND lastname=:lastname") \
            .params(firstname=author.firstname, lastname=author.lastname)
        db.engine.execute(stmt2)
        db.session().commit()
        flash("Kirjailija poistettiin onnistuneesti.", 'success')
        return redirect(url_for('authors_index'))


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


# edit author info
@app.route("/authors/<firstname>/<lastname>/edit/", methods=["GET", "POST"])
@login_required(role='ANY')
def admin_author_edit_info(firstname, lastname):
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
            flash("Virheellinen syöte (kentät eivät saa sisältää pelkästään välilyöntejä). Ole hyvä ja yritä uudestaan.", 'warning')
            return render_template("authors/editinfo.html", author=author)

        # check for spaces in name
        if (len(firstname.split(" ")) > 1) or (len(lastname.split(" ")) > 1):
            flash("Ole hyvä ja poista välilyönnit kirjailijan etu- tai sukunimestä.", 'warning')
            return render_template("authors/editinfo.html", author=author)

        # check if author with the name already in database
        authornamequery = Author.check_if_author_in_database(firstname.upper(), lastname.upper())

        if authornamequery == 0:
            stmt = text("UPDATE author SET firstname=:firstname, lastname=:lastname WHERE id=:id") \
                .params(firstname=firstname, lastname=lastname, id=author.id)
            db.engine.execute(stmt)
            db.session().commit()
            flash("Kirjailijan tiedot muutettu onnistuneesti!", 'success')
            return redirect(url_for("author_info", firstname=firstname, lastname=lastname))

        else:
            flash("Kyseinen kirjailija on jo lisätty tietokantaan.", 'warning')
            return render_template("authors/editinfo.html", author=author)
