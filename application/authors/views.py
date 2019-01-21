from flask import redirect, render_template, request, url_for

from application import app, db
from application.authors.models import Author
from application.authors.forms import AuthorForm

@app.route("/authors/", methods=["GET"])
def authors_index():
    return render_template("authors/list.html", authors = Author.query.all())

@app.route("/authors/new/")
def authors_form():
    return render_template("authors/new.html", form = AuthorForm())

@app.route("/authors/", methods=["POST"])
def authors_create():
    form = AuthorForm(request.form)

    if not form.validate():
        return render_template("authors/new.html", form = form)

    a = Author(form.firstname.data, form.lastname.data)

    db.session().add(a)
    db.session().commit()

    return redirect(url_for("authors_index"))
