from sqlalchemy import Column, Integer, String
from database import Base

class VideoGenre(Base):
    __tablename__ = 'video_genres'

    id = Column(Integer, primary_key=True)
    video_id = Column(String(255))
    genre_id = Column(Integer)

    def __init__(self, video_id, genre_id):
        self.video_id = video_id
        self.genre_id = genre_id

    def __repr__(self):
        return "<User(video_id='%s', genre_id='%d')>" % (self.video_id, self.genre_id)