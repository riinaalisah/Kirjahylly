from application import db
from application.models import Base

from sqlalchemy.sql import text

users_books = db.Table('users_books',
                       db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                       db.Column('user_id', db.Integer, db.ForeignKey('account.id')),
                       db.Column('read', db.Boolean, default=False, nullable=False)
                       )
'''
users_roles = db.Table('users_roles',
                       db.Column('user_id', db.Integer, db.ForeignKey('account.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                       )
'''


class User(Base):
    __tablename__ = "account"

    #name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(9), nullable=False)

    mybooks = db.relationship("Book", secondary=users_books,
                              backref=db.backref('mybooks', lazy='dynamic'))

    '''
    myroles = db.relationship("Roles", secondary=users_roles,
                              backref=db.backref('myroles', lazy='dynamic'))
    '''

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

    '''
    @staticmethod
    def get_users_roles(userid):

        stmt = text("select rolename from roles join users_roles ur on roles.id=ur.role_id and ur.user_id=:userid").params(userid=userid)

        res = db.engine.execute(stmt)
        print("*****************", res.fetchone()[0])

        return res.fetchone()[0]
        '''

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


'''
class Roles(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(10), nullable=False)

    def __init__(self, rolename):
        self.roleName = rolename
'''
