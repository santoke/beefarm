import redis

from app.path_helper import PathHelper
from app.config import Config
from pyquery import PyQuery as pq

class Document(object):

    def __init__(self):
        self.path_helper = PathHelper(Config.d['language'])
        self.redis = redis.StrictRedis(host=Config.d['redis']['address'], port=Config.d['redis']['port'], db=Config.d['redis']['db'])

    def pydoc(self, url):
        url = self.path_helper.page_url(url)

        pydoc = None
        try:
            pydoc = pq(url=url)
        except Exception as ex:
            print('error get url', url, ex)

        return pydoc

    # 읽어올 장르별 페이지
    def get_genre_list_page_links(self):
        max_thread = Config.d['parser_threads']
        pydoc = self.pydoc('genres.php')

        if pydoc == None:
            print("장르 목록 읽기 오류")
            return

        # 장르 리스트를 스레드 개수 만큼 나누어 담는다
        genre_url_hash = {}
        thread_idx = 0
        genre_urls = []
        for a_element in pydoc('.genreitem').find('a'):
            a_url = pq(a_element).attr('href')
            if thread_idx not in genre_url_hash.keys():
                genre_url_hash[thread_idx] = []
            genre_url_hash[thread_idx].append(a_url)
            thread_idx = (thread_idx + 1) % max_thread

        genre_count = 0
        for hash_key in genre_url_hash:
            for genre_url in genre_url_hash[hash_key]:
                genre_count = genre_count + 1
                genre_urls.append(genre_url)
        print("total genre count:", genre_count)
        return genre_urls

    # 장르별 페이징 번호 링크
    def get_video_last_paging_links(self, genre_url):
        htmldoc = None
        for i in range(1, 3):
            htmldoc = self.pydoc(genre_url)
            if htmldoc != None:
                break
            else:
                print("비디오 페이징 읽기 재시도중:", i)

        attr = htmldoc.find('.page.last').attr('href')
        last_link = None
        if attr != None:
            last_link = htmldoc.find('.page.last').attr('href')
        else:
            print('페이징 읽기 오류')
            #log_error_url(list_url)
        return last_link

    # 페이징 순회 (거꾸로)
    def iterate_paging(self, last_link, cache_start_page=3):
        arr_href = last_link.split('=')
        last_page = int(arr_href[-1])
        for i in reversed(range(2, last_page + 1)):
            url = '='.join(arr_href[0:-1]) + '=' + str(i)
            redis_key = f'complete_video_list:{url}'
            if i >= cache_start_page and self.redis.get(redis_key) != None:  # 이미 완료된 리스트 페이지
                print("======================cached list=================:", url)
                continue
            htmldoc = self.pydoc(url)
            if htmldoc != None:
                get_video_detail(htmldoc)
            self.redis.set(redis_key, 1);

        get_video_detail(htmldoc)
        print("$$$$$$$$$$===================", last_link, "=======================$$$$$$$$$$$$$$")

    # 비디오 상세 페이지
    def get_video_detail(list_html):
        for video_element in list_html('.videos').find('.video'):
            url = get_sub_uri(pq(video_element).find('a').attr('href'))
            pydoc = self.pydoc(url)
            if pydoc != None:
                print('need to insert')
                #doc = ModelHelper(pydoc, url)
                #doc.start_parse()