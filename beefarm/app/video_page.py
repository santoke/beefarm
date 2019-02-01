from app.html_parser import HTMLParser
from app.config import Config
from app.video_dao import VideoDAO
from request import ullib as rq

class VideoPage(HTMLParser):
    def __init__(self, url):
        super().__init__()

        self.url = url
        self.dao = VideoDAO()

        doc = self.pydoc(self.url)
        self.content_area = doc('#rightcolumn')
        self.jacket_info = self.content_area('#video_jacket_info')

    def set_video_id(self):
        video_id = self.jacket_info('#video_id').find('.text').text()
        self.video_id = video_id
        print('video id:', video_id)

    def get_id_and_name(self, element):
        code = element.attr('id')
        name = element.text()
        return code, name

    def parse_data(self):
        title = self.content_area('#video_title').text()
        release_date = self.jacket_info('#video_date').find('.text').text()
        video_length = self.jacket_info('#video_length').find('.text').text()

        video = self.dao.add_if_not_exist(self.vset_video_id)
        vide.site_url = self.site_url
        video.title = title
        video.cover_url = cover_url
        video.release_date = release_date
        video.video_length = video_length

        print('title:', title, ',release:', release_date, ', video_length:', video_length)

        #director
        #code, name = self.get_id_and_name(jacket_info('#video_director').find('.director'))
        #video.director_id = self.create_item_record('director', code, name).id
        #print('director:', code, name)

        #maker
        #code, name = self.get_id_and_name(jacket_info('#video_maker').find('.maker'))
        #video.maker_id = self.create_item_record('maker', code, name).id
        #print('maker:', code, name)

        #label
        #code, name = self.get_id_and_name(jacket_info('#video_label').find('.label'))
        #video.label_id = self.create_item_record('label', code, name).id
        #print('label:', code, name)

        #genres
        #print('genres')
        #jacket_info('#video_genres').find('.genre').each(self.iter_genres)

        #actors
        #print('actors')
        #jacket_info('#video_cast').find('.cast').each(self.iter_actor)

        self.dao.commit()
        self.download_cover(jacket_info)
        self.redis.set(f'{self.url}:visited', 1)

    def download_cover(self, jacket_info):
        cover_url = jacket_info('#video_jacket_img').attr('src')
        if (cover_url is not None) and Config.d['download_cover']:
            try:
                req.urlretrieve(jacket_info('#video_jacket_img').attr('src').replace("http", "https"), "covers/" + video_id + "." + (cover_url.split(".")[-1:][0]))
            except:
                print("cover download error")