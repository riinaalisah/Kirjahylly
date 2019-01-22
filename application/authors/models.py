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

    books = db.relationship("Book", secondary=authors_books, 
        backref=db.backref('books', lazy='dynamic'))


    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

