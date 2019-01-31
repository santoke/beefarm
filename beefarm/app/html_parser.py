import redis

from pyquery import PyQuery as pq
from app.config import Config
from app.path_helper import PathHelper

class HTMLParser:
    def __init__(self):
        self.path_helper = PathHelper(Config.d['language'])
        self.redis = redis.StrictRedis(host=Config.d['redis']['address'], port=Config.d['redis']['port'], db=Config.d['redis']['db'], password=Config.d['redis']['password'])

    def pydoc(self, url):
        url = self.path_helper.page_url(url)

        pydoc = None
        try:
            pydoc = pq(url=url)
        except Exception as ex:
            print('error get url', url, ex)

        return pydoc