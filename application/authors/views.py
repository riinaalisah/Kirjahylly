from flask import redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import text

from application import app, db, login_required
from application.authors.models import Author
from application.authors.forms import AuthorForm


@app.route("/authors/", methods=["GET"])
def authors_index():
    stmt = text("SELECT * FROM author ORDER BY books_count DESC")
    authors = db.engine.execute(stmt)
    return render_template("authors/list.html", authors=authors)


@app.route("/authors/new/")
@login_required(role="user")
def authors_form():
    return render_template("authors/new.html", form=AuthorForm())


@app.route("/authors/", methods=["POST"])
@login_required(role="user")
def authors_create():
    form = AuthorForm(request.form)

    if not form.validate():
        return render_template("authors/new.html", form=form)

    a = Author(form.firstname.data, form.lastname.data)

    db.session().add(a)
    db.session().commit()

    return redirect(url_for("authors_index"))
