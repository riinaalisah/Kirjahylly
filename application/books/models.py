from application import db
from application.models import Base


class Book(Base):

    name = db.Column(db.String(144), nullable=False)
    pages = db.Column(db.Integer(), nullable=True)
    isbn = db.Column(db.String(19), nullable=True)

    def __init__(self, name, pages, isbn):
        self.name = name
        self.pages = pages
        self.isbn = isbn
