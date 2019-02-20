from sqlalchemy import text, UniqueConstraint

from application import db
from application.models import Base

authors_books = db.Table('authors_books',
                         db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                         db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
                         )


class Author(Base):
    __tablename__ = "author"

    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    books_count = db.Column(db.Integer, nullable=False, default=0)
    __table_args__ = (db.UniqueConstraint('firstname', 'lastname', name='_author_name_uc'), )

    books = db.relationship("Book", secondary=authors_books,
                            backref=db.backref('books', lazy='dynamic'))

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.books_count = 0

    @staticmethod
    def all_authors():
        stmt = text("SELECT * FROM author")
        res = db.engine.execute(stmt)
        return res.fetchall()

    @staticmethod
    def author_firstnames():
        stmt = text("SELECT firstname FROM author")
        res = db.engine.execute(stmt)
        list = []
        for r in res:
            list.append(r)

        return list

    @staticmethod
    def author_lastnames():
        stmt = text("SELECT lastname FROM author")
        res = db.engine.execute(stmt).fetchall()
        list = []
        for r in res:
            list.append(r)

        return list
