from sqlalchemy import Column, Integer, String
from database import ModelBase

class Director(ModelBase):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    code = Column(String(255))
    name = Column(String(255))

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return "<User(code='%s', name='%s')>" % (self.code, self.name)