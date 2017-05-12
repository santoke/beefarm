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

    def __init__(self, pydoc):
        self.pydoc = pydoc

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

    def list_cast(index, node):
        d = pq(node)
        id = d.attr('id')
        name = d.find('.star').text()
        alias = d.find('.alias').text()
        print(id, name, alias)

    def list_comment(index, node):
        d = pq(node)
        id = d.attr('id')
        print(id)
        #print(d('.t').html().split('[img]'))

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
        record = db_session.query(ModelClass).filter_by(**{'video_id':self.video_id, 'genre_id':item_id}).first()
        if record == None:
            record = ModelClass(self.video_id, item_id)
            db_session.add(record)
            db_session.commit()
        return record

    def parse_doc(self, *args):
        has_video_record = False

        doc = self.pydoc
        content_area = doc('#rightcolumn')

        title = content_area('#video_title').text()
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
            req.urlretrieve(jacket_info('#video_jacket_img').attr('src'), "covers/" + video_id + "." + (cover_url.split(".")[-1:][0]))

        #release date
        release_date = jacket_info('#video_date').find('.text').text()
        print('release date:', release_date)

        #video length
        video_length = jacket_info('#video_length').find('.text').text()
        print('video_length:', video_length)

        video = db_session.query(Video).filter_by(id=video_id).first()

        if video == None:
            video = Video(video_id, title, cover_url, release_date, video_length)
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
        #print('cast')
        #jacket_info('#video_cast').find('.cast').each(list_cast)
        #print('comments')
        #content_area('#video_comments').find('.comment').each(list_comment)