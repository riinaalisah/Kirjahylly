from application import db
from application.models import Base

users_books = db.Table('users_books',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('account.id'))
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

