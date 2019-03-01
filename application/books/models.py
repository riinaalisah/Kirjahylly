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
                    " JOIN author a ON ab.author_id=a.id WHERE UPPER(b.name)=:bookname AND a.id=:authorid") \
            .params(bookname=bookname.upper(), authorid=authorid)
        res = db.engine.execute(stmt).fetchone()[0]
        return res

    @staticmethod
    def book_set_read(userid, bookid):
        stmt = text("UPDATE users_books SET read = '1' WHERE book_id = :book_id AND user_id = :user_id") \
            .params(user_id=userid, book_id=bookid)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def book_set_unread(userid, bookid):
        stmt = text("UPDATE users_books SET read = '0' WHERE book_id = :book_id AND user_id = :user_id") \
            .params(user_id=userid, book_id=bookid)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def book_delete_from_user(userid, bookid):
        stmt = text("DELETE FROM users_books WHERE user_id = :user_id AND book_id = :book_id") \
            .params(user_id=userid, book_id=bookid)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def book_update_info(name, year, pages, isbn, bookid):
        stmt = text("UPDATE book SET name=:bookname, year=:year, pages=:pages, isbn=:isbn WHERE id=:bookid") \
            .params(bookname=name, year=year, pages=pages, isbn=isbn, bookid=bookid)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def update_authorsbooks(newauthorid, currentauthorid, bookid):
        stmt = text("UPDATE authors_books SET author_id=:authorid"
                    " WHERE author_id=:currentauthorid AND book_id=:bookid") \
            .params(authorid=newauthorid, currentauthorid=currentauthorid, bookid=bookid)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def delete_from_authorsbooks(bookid):
        stmt = text("DELETE FROM authors_books WHERE book_id=:bookid").params(bookid=bookid)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def delete_from_usersbooks(bookid):
        stmt = text("DELETE FROM users_books WHERE book_id=:bookid").params(bookid=bookid)
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def delete_book(bookname, bookid):
        stmt = text("DELETE FROM book WHERE name=:bookname AND id=:bookid") \
            .params(bookname=bookname, bookid=bookid)
        db.engine.execute(stmt)
        db.session().commit()


    @staticmethod
    def delete_usersbooks_connection_todelete():
        stmt = text("DELETE FROM users_books WHERE book_id in (SELECT id FROM book WHERE name = 'TO-DELETE!!')")
        db.engine.execute(stmt)
        db.session().commit()

    @staticmethod
    def delete_books_todelete():
        stmt = text("DELETE FROM book WHERE name = 'TO-DELETE!!'")
        db.engine.execute(stmt)
        db.session().commit()

