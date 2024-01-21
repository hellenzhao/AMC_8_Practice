import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Category(db.Model):
    __table__ = db.Model.metadata.tables['category']

    def __repr__(self):
        return self.category
    
class Amc8(db.Model):
    __table__ = db.Model.metadata.tables['AMC_8']

    def __repr__(self):
        return self.content
    

