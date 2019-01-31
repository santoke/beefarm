from sqlalchemy import Column, Integer, String
from database import ModelBase

class VideoGenre(ModelBase):
    __tablename__ = 'video_genres'

    video_id = Column(String(255), primary_key=True)
    genre_id = Column(Integer, primary_key=True)

    def __init__(self, video_id, genre_id):
        self.video_id = video_id
        self.genre_id = genre_id

    def __repr__(self):
        return "<User(video_id='%s', genre_id='%d')>" % (self.video_id, self.genre_id)