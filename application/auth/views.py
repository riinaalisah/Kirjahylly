from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from application import app, db
from application.auth.models import User
from application.auth.models import users_books
from application.auth.forms import LoginForm
from application.auth.forms import UserForm
from application.books.models import Book

from sqlalchemy.sql import text

from application.views import index


@app.route("/auth/", methods=["GET"])
def auth_index():
    return render_template("auth/list.html", users=User.query.all())


@app.route("/auth/login/", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)
    # validoinnit

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form,
                               error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout/")
@login_required
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/new/")
def auth_form():
    return render_template("auth/new.html", form=UserForm())


@app.route("/auth/", methods=["POST"])
def auth_create():
    form = UserForm(request.form)

    if not form.validate():
        return render_template("auth/new.html", form=form)

    u = User(request.form.get("name"), request.form.get("username"), request.form.get("password"))

    db.session().add(u)
    db.session().commit()
    return redirect(url_for("auth_login"))


@app.route("/auth/info/", methods=["GET"])
@login_required
def auth_info():

    stmt = text(
        "SELECT ub.book_id, ub.user_id, author.firstname, author.lastname, ub.read, b.name "
        "FROM users_books ub JOIN book b ON b.id=ub.book_id, authors_books ab "
        "JOIN author ON author.id=ab.author_id WHERE ub.user_id=:user_id AND ab.book_id=ub.book_id").params(
        user_id=current_user.id)

    bookslist = db.engine.execute(stmt)
    db.session().commit()

    return render_template("auth/userinfo.html", user=current_user, books=bookslist,
                           all_books=current_user.count_all_books(current_user.id),
                           read_books=current_user.count_read_books(current_user.id))


@app.route("/auth/info/<book_id>/", methods=["POST"])
@login_required
def books_set_read_or_delete(book_id):

    if request.form["btn"] == "Merkitse luetuksi":

        stmt = text("UPDATE users_books SET read = \"true\" WHERE book_id = :book_id AND user_id = :user_id") \
            .params(user_id=current_user.id, book_id=book_id)

    elif request.form["btn"] == "Merkitse lukemattomaksi":
        stmt = text("UPDATE users_books SET read = \"false\" WHERE book_id = :book_id AND user_id = :user_id") \
            .params(user_id=current_user.id, book_id=book_id)

    else:
        stmt = text("DELETE FROM users_books WHERE user_id = :user_id AND book_id = :book_id") \
            .params(user_id=current_user.id, book_id=book_id)

    db.engine.execute(stmt)
    db.session().commit()

    return redirect(url_for("auth_info"))

@app.route("/auth/edit/", methods=["GET", "POST"])
@login_required
def auth_edit_form():

    if request.method == "GET":
        return render_template("auth/editinfo.html", form=UserForm())

    elif request.method == "POST" and request.form["btn"] == "Poista käyttäjätili":
        #logout_user()
        stmt = text("DELETE FROM account WHERE id=:userid").params(userid=current_user.id)
        db.engine.execute(stmt)
        db.session().commit()
        return redirect(url_for("index"))

    else:
        modifieduser = User(request.form.get("name"), request.form.get("username"), request.form.get("password"))
        if modifieduser.name != "":
            current_user.name = modifieduser.name

        if modifieduser.username != "":
            current_user.username = modifieduser.username

        if modifieduser.password != "":
            current_user.password = modifieduser.password

        db.session().commit()
        return redirect(url_for('auth_info', username=current_user.username))

