from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, current_user, login_user

from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm
from application.auth.forms import UserForm

from sqlalchemy.sql import text

from passlib.hash import sha256_crypt


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
        flash("Syötetty käyttäjänimi tai salasana ei täsmää.", 'warning')
        return render_template("auth/loginform.html", form=form)

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout/")
@login_required(role="user")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/new/")
def auth_form():
    return render_template("auth/new.html", form=UserForm())


@app.route("/auth/register/", methods=["GET", "POST"])
def auth_register():
    try:
        # form = RegistrationForm(request.form)
        form = request.form

        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = sha256_crypt.encrypt((str(request.form["password"])))
            passwordagain = sha256_crypt.encrypt((str(request.form["passwordagain"])))

            '''
            if password != passwordagain:
                flash("Salasanan varmistus epäonnistui, yritä uudelleen.", 'warning')
                return render_template("auth/register.html", form=form)
            '''

            stmt = text("SELECT cast(count(id) as unsigned) FROM account WHERE username=:username").params(username=username)
            res = db.engine.execute(stmt).fetchone()[0]
            print("***************************", res)

            if res > 0:
                flash("Käyttäjänimi on jo käytössä, ole hyvä ja valitse toinen.", 'warning')
                return render_template("auth/register.html", form=form)

            else:
                user = User(username=username, email=email, password=password, role='user')
                db.session().add(user)
                db.session().commit()
                flash("Rekisteröityminen onnistui, tervetuloa!", 'success')

                login_user(user)

                return redirect(url_for('index'))

        return render_template("auth/register.html", form=form)

    except Exception as e:
        return (str(e))


@app.route("/auth/", methods=["POST"])
def auth_create():
    form = UserForm(request.form)

    if not form.validate():
        return render_template("auth/new.html", form=form)

    u = User(request.form.get("name"), request.form.get("username"), request.form.get("password"), "user")

    db.session().add(u)
    db.session().commit()
    return redirect(url_for("auth_login"))


@app.route("/auth/info/", methods=["GET"])
@login_required(role="user")
def auth_info():
    stmt_unread = text(
        "SELECT ub.book_id, ub.user_id, author.firstname, author.lastname, ub.read, b.name "
        "FROM users_books ub JOIN book b ON b.id=ub.book_id, authors_books ab "
        "JOIN author ON author.id=ab.author_id WHERE ub.user_id=:user_id AND ab.book_id=ub.book_id AND read = '0'").params(
        user_id=current_user.id)

    unread_books = db.engine.execute(stmt_unread)

    stmt_read = text(
        "SELECT ub.book_id, ub.user_id, author.firstname, author.lastname, ub.read, b.name "
        "FROM users_books ub JOIN book b ON b.id=ub.book_id, authors_books ab "
        "JOIN author ON author.id=ab.author_id WHERE ub.user_id=:user_id AND ab.book_id=ub.book_id AND read = '1'").params(
        user_id=current_user.id)

    read_books = db.engine.execute(stmt_read)

    return render_template("auth/userinfo.html", user=current_user, unread=unread_books, read=read_books,
                           all_books=current_user.count_all_books(current_user.id),
                           read_books=current_user.count_read_books(current_user.id))


@app.route("/auth/info/<book_id>/", methods=["POST"])
@login_required(role="user")
def books_set_read_or_delete(book_id):
    if request.form["btn"] == "Merkitse luetuksi":

        stmt = text("UPDATE users_books SET read = '1' WHERE book_id = :book_id AND user_id = :user_id") \
            .params(user_id=current_user.id, book_id=book_id)

    elif request.form["btn"] == "Merkitse lukemattomaksi":
        stmt = text("UPDATE users_books SET read = '0' WHERE book_id = :book_id AND user_id = :user_id") \
            .params(user_id=current_user.id, book_id=book_id)

    else:
        stmt = text("DELETE FROM users_books WHERE user_id = :user_id AND book_id = :book_id") \
            .params(user_id=current_user.id, book_id=book_id)

    db.engine.execute(stmt)
    db.session().commit()

    return redirect(url_for("auth_info"))


@app.route("/auth/edit/", methods=["GET", "POST"])
@login_required(role="user")
def auth_edit_form():
    if request.method == "GET":
        return render_template("auth/editinfo.html", form=UserForm())

    elif request.method == "POST" and request.form["btn"] == "Poista käyttäjätili":
        # logout_user()
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
