from sqlalchemy import text

from application import db
from application.models import Base


class Book(Base):

    name = db.Column(db.String(40), nullable=False)
    year = db.Column(db.String(4), nullable=True)
    pages = db.Column(db.String(4), nullable=True)
    isbn = db.Column(db.String(19), nullable=True)

    def __init__(self, name, year, pages, isbn):
        self.name = name
        self.year = year
        self.pages = pages
        self.isbn = isbn


    @staticmethod
    def all_books():
        stmt = text("SELECT book_id, author_id, name, firstname, lastname FROM authors_books JOIN book ON "
                    "book.id=authors_books.book_id JOIN author ON author.id=authors_books.author_id ORDER BY name ASC")
        res = db.engine.execute(stmt)
        return res

    @staticmethod
    def book_info(bookid):
        stmt = text("SELECT book.id, book.name, book.year, book.pages, book.isbn, author.firstname, author.lastname "
                "FROM book JOIN authors_books ab ON ab.book_id=book.id JOIN author ON ab.author_id=author.id "
                "WHERE book.id = :bookid").params(bookid=bookid)
        res = db.engine.execute(stmt).fetchone()
        return res

    @staticmethod
    def check_if_book_with_name_and_authorid_exists(bookname, authorid):
        stmt = text("SELECT COUNT(b.id) FROM book b JOIN authors_books ab ON ab.book_id=b.id"
                    " JOIN author a ON ab.author_id=a.id WHERE UPPER(b.name)=:bookname AND a.id=:authorid")\
            .params(bookname=bookname.upper(), authorid=authorid)
        res = db.engine.execute(stmt).fetchone()[0]
        return res
