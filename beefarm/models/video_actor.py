from sqlalchemy import Column, Integer, String
from database import Base

class VideoActor(Base):
    __tablename__ = 'video_actors'

    id = Column(Integer, primary_key=True)
    video_id = Column(String(255))
    actor_id = Column(Integer)

    def __init__(self, video_id, actor_id):
        self.video_id = video_id
        self.actor_id = actor_id

    def __repr__(self):
        return "<User(video_id='%s', genre_id='%d')>" % (self.video_id, self.actor_id)