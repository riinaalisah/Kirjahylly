import uuid

from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, current_user, login_user
from flask_mail import Message

from application import app, db, login_required, mail
from application.auth.models import User
from application.auth.forms import UserForm

from sqlalchemy.sql import text

from passlib.hash import sha256_crypt


@app.route("/auth/", methods=["GET"])
def auth_index():
    return render_template("auth/list.html", users=User.query.all())


@app.route("/auth/login/", methods=["GET", "POST"])
def auth_login():
    try:
        if request.method == "POST":

            stmt = text("SELECT * FROM account WHERE username=:username").params(username=request.form['username'])

            res = db.engine.execute(stmt)
            data = res.fetchone()[5]

            if sha256_crypt.verify(request.form['password'], data):
                user = User.query.filter_by(username=request.form['username']).first()
                login_user(user)

                flash("Sisäänkirjautuminen onnistui!", 'success')
                return redirect(url_for('index'))

            else:
                flash("Käyttäjänimi tai salasana ei täsmää, yritä uudelleen.", 'warning')

        return render_template("auth/loginform.html")


    except Exception:
        flash("Käyttäjänimi tai salasana ei täsmää, yritä uudelleen.", 'warning')
        return render_template("auth/loginform.html")


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
        form = request.form

        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            passwordagain = request.form["passwordagain"]

            if password != passwordagain:
                flash("Salasanan varmistus epäonnistui, yritä uudelleen.", 'warning')
                return render_template("auth/register.html", form=form)

            stmt = text("SELECT count(id) FROM account WHERE username=:username").params(username=username)
            res = db.engine.execute(stmt).fetchone()[0]

            emailres = User.query.filter_by(email=email).first()

            if res > 0:
                flash("Kyseinen käyttäjänimi on jo käytössä, ole hyvä ja valitse toinen.", 'warning')
                return render_template("auth/register.html", form=form)

            elif emailres is not None:
                flash("Kyseinen sähköpostiosoite on jo käytössä, ole hyvä ja valitse toinen.", 'warning')
                return render_template("auth/register.html", form=form)

            else:
                password = sha256_crypt.encrypt((str(request.form["password"])))
                user = User(username=username, email=email, password=password, role='user')
                db.session().add(user)
                db.session().commit()
                flash("Rekisteröityminen onnistui, tervetuloa!", 'success')

                login_user(user)

                return redirect(url_for('index'))

        return render_template("auth/register.html", form=form)

    except Exception as e:
        return (str(e))

# unnecessary method?
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
    return render_template("auth/userinfo.html", user=current_user,
                           unread=current_user.get_unread_books(current_user.id),
                           read=current_user.get_read_books(current_user.id),
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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Salasanan vaihtaminen',
                  sender='rrraa96@gmail.com',
                  recipients=[user.email])

    msg.body = f'''Vaihtaaksesi salasanasi, käytä seuraavaa linkkiä:
{url_for('auth_reset_token', token=token, _external=True)}

Jos et ole pyytänyt salasananvaihtoa, ole hyvä ja jätä tämä viesti huomiotta.
'''
    mail.send(msg)


@app.route("/auth/reset_password", methods=["GET", "POST"])
def auth_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = request.form

    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if user is None:
            flash("Kyseisellä sähköpostiosoitteella ei löytynyt käyttäjätiliä, yritä uudestaan.", 'warning')
            return redirect(url_for('auth_reset_request'))
        send_reset_email(user)
        flash("Sähköpostiviesti lähetetty salasanan vaihtoa varten.", 'info')
        return redirect(url_for('auth_login'))

    return render_template('/auth/reset_request.html', form=form)


@app.route("/auth/reset_password/<token>", methods=["GET", "POST"])
def auth_reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash("Virheellinen tai vanhentunut valtuus (token)", 'warning')
        return render_template(url_for('auth_reset_request'))

    form = request.form

    if request.method == "POST":
        hashed_password = sha256_crypt.encrypt((str(request.form["password"])))
        user.password = hashed_password
        db.session().commit()
        flash("Salasanasi on vaihdettu onnistuneesti! Voit nyt kirjautua sisään.", 'success')
        return redirect(url_for('auth_login'))

    return render_template('auth/reset_token.html', form=form)
