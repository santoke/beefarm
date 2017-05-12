import urllib.request as req
import threading
import importlib

from pyquery import PyQuery as pq
from database import db_session
from models.video import Video
from models.actor import Actor
from models.director import Director
from models.genre import Genre
from models.label import Label
from models.maker import Maker
from models.video_genre import VideoGenre

class Document:
    video_id = ''
    site_url = ''

    def __init__(self, pydoc, site_url):
        self.pydoc = pydoc
        self.site_url = site_url

    def start_parse(self):
        thread = threading.Thread(target=self.parse_doc, args=(1, 1))
        thread.start()

    def iter_genres(self, index, node):
        d = pq(node)
        code = d.attr('id')
        name = d.text()
        genre = self.create_item_record('genre', code, name)
        video_genre = self.create_relation_record('video_genre', genre.id)
        print(code, name, video_genre.id)

    def iter_actor(self, index, node):
        d = pq(node)
        code = d.attr('id')
        name = d.find('.star').text()
        alias = d.find('.alias').text()
        actor = db_session.query(Actor).filter_by(code=code).first()
        if actor == None:
            actor = Actor(code, name, alias)
            db_session.add(actor)
            db_session.commit()
        video_actor = self.create_relation_record('video_actor', actor.id)
        print(code, name, alias, video_actor.id)

    def get_id_and_name(self, element):
        code = element.attr('id')
        name = element.text()
        return code, name

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
        record = db_session.query(ModelClass).filter_by(**{'video_id':self.video_id, last_word + '_id':item_id}).first()
        if record == None:
            record = ModelClass(self.video_id, item_id)
            db_session.add(record)
            db_session.commit()
        return record

    def parse_doc(self, *args):
        has_video_record = False

        doc = self.pydoc
        content_area = doc('#rightcolumn')

        #title
        title = content_area('#video_title').text().encode('utf-8')
        print('title is:', title)

        jacket_info = content_area('#video_jacket_info')

        #video id
        video_id = jacket_info('#video_id').find('.text').text()
        self.video_id = video_id
        print('video id is:', video_id)

        #image download
        cover_url = jacket_info('#video_jacket_img').attr('src')
        print('jacket image url:', cover_url)
        if cover_url is not None:
            try:
                req.urlretrieve(jacket_info('#video_jacket_img').attr('src'), "covers/" + video_id + "." + (cover_url.split(".")[-1:][0]))
            except:
                print("cover download error")

        #release date
        release_date = jacket_info('#video_date').find('.text').text()
        print('release date:', release_date)

        #video length
        video_length = jacket_info('#video_length').find('.text').text()
        print('video_length:', video_length)

        video = db_session.query(Video).filter_by(id=video_id).first()

        if video == None:
            video = Video(video_id, self.site_url, title, cover_url, release_date, video_length)
            has_video_record = False
        else:
            has_video_record = True

        #director
        code, name = self.get_id_and_name(jacket_info('#video_director').find('.director'))
        video.director_id = self.create_item_record('director', code, name).id
        print('director:', code, name)

        #maker
        code, name = self.get_id_and_name(jacket_info('#video_maker').find('.maker'))
        video.maker_id = self.create_item_record('maker', code, name).id
        print('maker:', code, name)

        #label
        code, name = self.get_id_and_name(jacket_info('#video_label').find('.label'))
        video.label_id = self.create_item_record('label', code, name).id
        print('label:', code, name)

        if has_video_record == False:
            db_session.add(video)
        db_session.commit()

        #genres
        print('genres')
        jacket_info('#video_genres').find('.genre').each(self.iter_genres)

        #actors
        print('actor')
        jacket_info('#video_cast').find('.cast').each(self.iter_actor)