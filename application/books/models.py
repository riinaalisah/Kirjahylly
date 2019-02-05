from application import db
from application.models import Base


class Book(Base):

    name = db.Column(db.String(144), nullable=False)

    def __init__(self, name):
        self.name = name
        # self.read = False
