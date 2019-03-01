from sqlalchemy import text

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
    __table_args__ = (db.UniqueConstraint('firstname', 'lastname', name='_author_name_uc'),)

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
    def all_author_by_bookcount():
        stmt = text("SELECT * FROM author ORDER BY books_count DESC")
        res = db.engine.execute(stmt)
        return res

    @staticmethod
    def authors_books_by_author_name(firstname, lastname):
        stmt = text("SELECT a.id, a.firstname, a.lastname, ab.book_id, b.name FROM author a"
                    " JOIN authors_books ab ON ab.author_id=a.id"
                    " JOIN book b ON ab.book_id=b.id"
                    " WHERE a.firstname=:firstname AND a.lastname=:lastname") \
            .params(firstname=firstname, lastname=lastname)
        res = db.engine.execute(stmt)
        return res.fetchall()

    @staticmethod
    def check_if_author_in_database(firstname, lastname):
        authornamequery = text("SELECT COUNT(id) FROM author WHERE UPPER(firstname)=:firstname"
                               " AND UPPER(lastname)=:lastname") \
            .params(firstname=firstname.upper(), lastname=lastname.upper())
        res = db.engine.execute(authornamequery)
        return res.fetchone()[0]

    @staticmethod
    def change_booknames_todelete(authorid):
        stmt = text("UPDATE book SET name = 'TO-DELETE!!'"
                    " WHERE book.id IN (SELECT book_id FROM authors_books WHERE author_id = :authorid)") \
            .params(authorid=authorid)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def delete_authorsbooks_connection(authorid):
        stmt = text("DELETE FROM authors_books WHERE author_id=:authorid").params(authorid=authorid)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def delete_author(firstname, lastname):
        stmt = text("DELETE FROM author WHERE firstname=:firstname AND lastname=:lastname") \
            .params(firstname=firstname, lastname=lastname)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def update_authorinfo(firstname, lastname, authorid):
        stmt = text("UPDATE author SET firstname=:firstname, lastname=:lastname WHERE id=:authorid") \
            .params(firstname=firstname, lastname=lastname, authorid=authorid)
        db.engine.execute(stmt)
        db.session().commit()