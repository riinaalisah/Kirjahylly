from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from application import db, login_manager, app
from application.models import Base

from sqlalchemy.sql import text


@login_manager.user_loader
def get_user(user_id):
    user = User.query.get(user_id).first()
    if user:
        return user
    return None


users_books = db.Table('users_books',
                       db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                       db.Column('user_id', db.Integer, db.ForeignKey('account.id')),
                       db.Column('read', db.Boolean, default=False, nullable=False)
                       )


class User(Base, UserMixin):
    __tablename__ = "account"

    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(90), nullable=False)
    role = db.Column(db.String(9), nullable=False)

    mybooks = db.relationship("Book", secondary=users_books,
                              backref=db.backref('mybooks', lazy='dynamic'))

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __repr__(self):
        return f"User('{self.username}', '{self.email}, '{self.role}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']

        except:
            return None

        return User.query.get(user_id)

    @staticmethod
    def count_all_books(userid):
        stmt = text("SELECT COUNT(users_books.book_id) FROM users_books WHERE user_id = :userid").params(userid=userid)

        res = db.engine.execute(stmt)
        return res.fetchone()[0]

    @staticmethod
    def count_read_books(userid):
        stmt = text("SELECT COUNT(users_books.book_id) FROM users_books WHERE user_id = :userid AND read = '1'").params(
            userid=userid)

        res = db.engine.execute(stmt)
        return res.fetchone()[0]

    @staticmethod
    def get_user_by_username(username):
        stmt = text("SELECT * FROM account WHERE username=:username").params(username=username)
        res = db.engine.execute(stmt)
        return res

    @staticmethod
    def get_read_books(userid):
        stmt = text(
            "SELECT ub.book_id, ub.user_id, author.firstname, author.lastname, ub.read, b.name "
            "FROM users_books ub JOIN book b ON b.id=ub.book_id, authors_books ab "
            "JOIN author ON author.id=ab.author_id WHERE ub.user_id=:user_id AND ab.book_id=ub.book_id AND read = '1'").params(
            user_id=userid)

        res = db.engine.execute(stmt)
        return res

    @staticmethod
    def get_unread_books(userid):
        stmt = text(
            "SELECT ub.book_id, ub.user_id, author.firstname, author.lastname, ub.read, b.name "
            "FROM users_books ub JOIN book b ON b.id=ub.book_id, authors_books ab "
            "JOIN author ON author.id=ab.author_id WHERE ub.user_id=:user_id AND ab.book_id=ub.book_id AND read = '0'").params(
            user_id=userid)

        res = db.engine.execute(stmt)
        return res

    @staticmethod
    def get_users_books(userid):
        stmt = text("SELECT book_id FROM users_books WHERE user_id=:userid").params(userid=userid)
        res = db.engine.execute(stmt).fetchall()
        resultset = []
        for row in res:
            resultset.append(row[0])

        return resultset

    @staticmethod
    def count_users_with_username(username):
        stmt = text("SELECT count(id) FROM account WHERE username=:username").params(username=username)
        res = db.engine.execute(stmt).fetchone()[0]
        return res

    @staticmethod
    def count_users_with_email(email):
        stmt = text("SELECT count(id) FROM account WHERE email=:email").params(email=email)
        res = db.engine.execute(stmt).fetchone()[0]
        return res

    @staticmethod
    def delete_usersbooks_connection(userid):
        stmt = text("DELETE FROM users_books WHERE user_id=:userid").params(userid=userid)
        db.engine.execute(stmt)
        db.session().commit()


    @staticmethod
    def delete_user_by_username(username):
        stmt = text("DELETE FROM account WHERE username=:username").params(username=username)
        db.engine.execute(stmt)
        db.session().commit()