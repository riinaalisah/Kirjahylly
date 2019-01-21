from application import db
from application.models import Base

class Author(Base):

    firstname = db.Column(db.String(144), nullable=False)
    lastname = db.Column(db.String(144), nullable=False)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
