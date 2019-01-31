from sqlalchemy import Column, Integer, String
from database import ModelBase

class Actor(ModelBase):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    code = Column(String(255))
    name = Column(String(255))
    alias = Column(String(255))

    def __init__(self, code, name, alias):
        self.code = code
        self.name = name
        self.alias = alias

    def __repr__(self):
        return "<User(code='%s', name='%s')>" % (self.code, self.name)