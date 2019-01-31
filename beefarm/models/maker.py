from sqlalchemy import Column, Integer, String
from database import ModelBase

class Maker(ModelBase):
    __tablename__ = 'makers'

    id = Column(Integer, primary_key=True)
    code = Column(String(255))
    name = Column(String(255))

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return "<User(code='%s', name='%s')>" % (self.code, self.name)