from application import db
from application.models import Base

from sqlalchemy.sql import text

users_books = db.Table('users_books',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('account.id')),
    db.Column('read', db.Boolean, default=False, nullable=False)
)

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    mybooks = db.relationship("Book", secondary=users_books,
        backref=db.backref('mybooks', lazy='dynamic'))

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def count_all_books(userid):
        stmt = text("SELECT COUNT(users_books.book_id) FROM users_books WHERE user_id = :userid").params(userid=userid)

        res = db.engine.execute(stmt)
        return res.fetchone()[0]


    @staticmethod
    def count_read_books(userid):
        stmt = text("SELECT COUNT(users_books.book_id) FROM users_books WHERE user_id =  :userid AND read = \"true\"").params(userid=userid)

        res = db.engine.execute(stmt)
        return res.fetchone()[0]
