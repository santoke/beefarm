import importlib

from database import Connection
from app.config import Config
from models.video import Video
from models.actor import Actor
from models.director import Director
from models.genre import Genre
from models.label import Label
from models.maker import Maker
from models.video_genre import VideoGenre

class VideoDAO:

    def __init__(self):
        Connection()
        self.session = Connection.session

    def iter_genres(self, index, node):
        d = pq(node)
        code = d.attr('id')
        name = d.text()
        genre = self.create_item_record('genre', code, name)
        video_genre = self.create_relation_record('video_genre', genre.id)
        print(code, name)

    def commit(self):
        self.session.commit()

    def get_video(self, video_id):
        video = self.session.query(Video).filter_by(id=video_id).first()
        return video

    def add_if_not_exist(self, video_id):
        video = self.get_video(video_id)
        if video == None:
            video = Video(video_id)
        return video

    def iter_actor(self, index, node):
        d = pq(node)
        code = d.attr('id')
        name = d.find('.star').text()
        alias = d.find('.alias').text()
        actor = self.session.query(Actor).filter_by(code=code).first()
        if actor == None:
            actor = Actor(code, name, alias)
            db_session.add(actor)
            db_session.commit()
        video_actor = self.create_relation_record('video_actor', actor.id)
        print(code, name, alias, video_actor.id)

    def create_item_record(self, file_name, code, name):
        ModelClass = getattr(importlib.import_module("models." + file_name), file_name.title())
        record = db_session.query(ModelClass).filter_by(code=code).first()
        if record == None:
            record = ModelClass(code, name)
            db_session.add(record)
            db_session.commit()
        return record

    def create_relation_record(self, file_name, item_id):
        class_name = ""
        last_word = ""
        for s in file_name.split("_"):
            class_name = class_name + s.title()
            last_word = s
        ModelClass = getattr(importlib.import_module("models." + file_name), class_name)
        record = self.session.query(ModelClass).filter_by(**{'video_id':self.video_id, last_word + '_id':item_id}).first()
        if record == None:
            record = ModelClass(self.video_id, item_id)
            db_session.add(record)
            db_session.commit()
        return record