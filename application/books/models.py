from application import db
from application.models import Base


class Book(Base):

    name = db.Column(db.String(144), nullable=False)

    #account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    #author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __init__(self, name):
        self.name = name
        # self.read = False
