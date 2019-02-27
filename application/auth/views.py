from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, current_user, login_user
from flask_mail import Message

from application import app, db, login_required, mail
from application.auth.models import User
from application.auth.forms import UserForm

from sqlalchemy.sql import text

from passlib.hash import sha256_crypt


@app.route("/auth/", methods=["GET"])
@login_required(role="admin")
def auth_all():
    return render_template("auth/list.html", users=User.query.all())


@app.route("/auth/delete/<username>", methods=["GET", "POST"])
@login_required(role='admin')
def admin_delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user.role == 'admin':
        flash("Admin-käyttäjiä ei voi poistaa.", 'info')
        return redirect(url_for('auth_all'))

    if request.method == "GET":
        return render_template("auth/deleteuser.html", user=user)

    else:
        stmt = text("DELETE FROM users_books WHERE user_id=:userid").params(userid=user.id)
        db.engine.execute(stmt)

        stmt2 = text("DELETE FROM account WHERE username=:username").params(username=username)
        db.engine.execute(stmt2)

        db.session().commit()
        flash("Käyttäjä poistettiin onnistuneesti.", 'success')
        return redirect(url_for('auth_all'))


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
@login_required(role="ANY")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


# unnecessary?
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
@login_required(role="ANY")
def auth_info():
    return render_template("auth/userinfo.html", user=current_user)


@app.route("/auth/info/edit/", methods=["GET", "POST"])
@login_required(role="ANY")
def auth_edit():
    if request.method == "GET":
        return render_template("auth/editinfo.html", user=current_user)

    if request.method == "POST":
        user = current_user
        username = request.form["username"]
        email = request.form["email"]
        changed = False

        # check if username is taken
        if user.username != username:
            stmt = text("SELECT count(id) FROM account WHERE username=:username").params(username=username)
            res = db.engine.execute(stmt).fetchone()[0]
            if res == 0:
                user.username = username
                changed = True
            else:
                flash("Kyseinen nimimerkki on jo käytössä, ole hyvä ja valitse toinen.", 'warning')
                return render_template("auth/editinfo.html", user=current_user)

        # check if email is taken
        if user.email != email:
            stmt = text("SELECT count(id) FROM account WHERE email=:email").params(email=email)
            res = db.engine.execute(stmt).fetchone()[0]
            if res == 0:
                user.email = email
                changed = True
            else:
                flash("Kyseinen sähköpostiosoite on jo käytössä, ole hyvä ja valitse toinen.", 'warning')
                return render_template("auth/editinfo.html", user=current_user)

        if changed:
            db.session().commit()
            flash("Tiedot päivitettiin onnistuneesti!", 'success')
            return redirect(url_for('auth_info', user=current_user))

        else:
            flash("Et muuttanut tietoja.", 'info')
            return render_template("auth/editinfo.html", user=current_user)


@app.route("/auth/info/edit/password", methods=["GET", "POST"])
@login_required(role="ANY")
def auth_change_password():
    if request.method == "GET":
        return render_template("auth/changepassword.html", user=current_user)

    else:
        user = current_user
        password = request.form["currentpassword"]
        newpassword = request.form["newpassword"]
        confirmpassword = request.form["confirmpassword"]

        if not sha256_crypt.verify(password, user.password) or newpassword != confirmpassword:
            flash("Salasanan varmistus epäonnistui, ole hyvä ja yritä uudestaan.", 'warning')
            return render_template("auth/changepassword.html", user=current_user)

        else:
            user.password = sha256_crypt.encrypt((str(newpassword)))
            db.session().commit()
            flash("Salasana vaihdettiin onnistuneesti!", 'success')
            return redirect(url_for('auth_info', user=current_user))


@app.route("/auth/mybooks/", methods=["GET"])
@login_required(role="ANY")
def auth_mybooks():
    return render_template("auth/mybooks.html", user=current_user,
                           unread=current_user.get_unread_books(current_user.id),
                           read=current_user.get_read_books(current_user.id),
                           all_books=current_user.count_all_books(current_user.id),
                           read_books=current_user.count_read_books(current_user.id))


@app.route("/auth/info/<book_id>/", methods=["POST"])
@login_required(role="ANY")
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

    return redirect(url_for("auth_mybooks"))


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
        flash("Virheellinen tai vanhentunut valtuus (token).", 'warning')
        return redirect(url_for('auth_reset_request'))

    form = request.form

    if request.method == "POST":
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]
        if password != confirmpassword:
            flash("Salasanan varmistus epäonnistui, ole hyvä ja yritä uudestaan.", 'warning')
            return redirect(url_for('auth_reset_token', token=token))

        else:
            hashed_password = sha256_crypt.encrypt((str(request.form["password"])))
            user.password = hashed_password
            db.session().commit()
            flash("Salasanasi on vaihdettu onnistuneesti! Voit nyt kirjautua sisään.", 'success')
            return redirect(url_for('auth_login'))

    return render_template('auth/reset_token.html', form=form)


@app.route("/auth/info/edit/delete/", methods=["GET", "POST"])
@login_required(role='user')
def auth_delete_user():
    if current_user.role == 'admin':
        flash("Admin-käyttäjiä ei voi poistaa.", 'info')
        return redirect(url_for('auth_edit'))

    if request.method == "GET":
        return render_template("auth/deleteownprofile.html")

    else:
        user = current_user

        stmt = text("DELETE FROM users_books WHERE user_id=:userid").params(userid=user.id)
        db.engine.execute(stmt)

        stmt2 = text("DELETE FROM account WHERE username=:username").params(username=user.username)
        db.engine.execute(stmt2)

        db.session().commit()
        flash("Käyttäjätili poistettiin onnistuneesti.", 'success')
        return redirect(url_for('index'))
