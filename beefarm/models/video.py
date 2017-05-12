from sqlalchemy import Column, Integer, String, CHAR
from database import Base

class Video(Base):
    __tablename__ = 'videos'

    id = Column(CHAR(12), primary_key=True)
    subject = Column(String(255))
    image = Column(String(255))
    release_date = Column(String(255))
    length = Column(Integer)

    director_id = Column(Integer)
    maker_id = Column(Integer)
    label_id = Column(Integer)

    def __init__(self, id, subject, image, release_date, length):
        self.id = id
        self.subject = subject
        self.image = image
        self.release_date = release_date
        self.length = length

    def __repr__(self):
        return "<User(id='%s', subject='%s', release_date='%s')>" % (self.id, self.subject, self.release_date)