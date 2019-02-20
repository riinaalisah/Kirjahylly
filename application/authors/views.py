from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user
from sqlalchemy import text

from application import app, db, login_required
from application.authors.models import Author


@app.route("/authors/", methods=["GET"])
def authors_index():
    stmt = text("SELECT * FROM author ORDER BY books_count DESC")
    authors = db.engine.execute(stmt)
    return render_template("authors/list.html", authors=authors)


@app.route("/authors/new", methods=["GET", "POST"])
@login_required(role="ANY")
def authors_create():

    if request.method == "GET":
        return render_template("authors/new.html")

    else:
        form = request.form
        firstname = request.form["firstname"].capitalize()
        lastname = request.form["lastname"].capitalize()

        a = Author(firstname, lastname)

        try:
            db.session().add(a)
            db.session().commit()
            flash("Kirjailija lisätty onnistuneesti!", 'success')
            return redirect(url_for("authors_index"))

        except Exception as e:
            flash("Kirjailija on jo lisätty tietokantaan.", 'warning')
            return redirect(url_for('authors_create'))

