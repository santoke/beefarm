from sqlalchemy import Column, String
from database import ModelBase

class Url(ModelBase):
    __tablename__ = 'urls'

    url = Column(String(255), primary_key=True)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<User(url='%s')>" % (self.url)