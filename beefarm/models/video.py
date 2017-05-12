from sqlalchemy import Column, Integer, String, CHAR
from database import Base

class Video(Base):
    __tablename__ = 'videos'

    id = Column(CHAR(12), primary_key=True)
    subject = Column(String(255))
    release_date = Column(String(255))
    length = Column(Integer)

    def __repr__(self):
        return "<User(id='%s', subject='%s', release_date='%s')>" % (self.id, self.subject, self.release_date)