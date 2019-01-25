import urllib.request as req
import redis
import threading
import time
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from app.model_helper import ModelHelper
from app.config import Config
from database import db_session
from models.url import Url
from models.error_url import ErrorUrl

Config()
redis = redis.StrictRedis(host=Config.d['redis']['addr'], port=Config.d['redis']['addr'], db=Config.d['redis']['db'])
last_touch_url = '';

def log_site_url(url):
    redis.set(url, 1)
    if db_session.query(Url).filter_by(url=url).first() == None:
        db_session.add(Url(url))
        db_session.commit()

def log_error_url(url):
    if db_session.query(ErrorUrl).filter_by(url=url).first() == None:
        db_session.add(ErrorUrl(url))
        db_session.commit()
    print("Get URL Error:", url)

def get_pydoc(url):
    url = Config.d['proxy'] + Config.d['domain'] + get_sub_uri(url)
    print("to get pydoc:", url)
    log_site_url(url)
    pydoc = None
    try:
        pydoc = pq(url=url)
    except Exception as ex:
        if db_session.query(ErrorUrl).filter_by(url=url).first() == None:
            log_error_url(url)
    return pydoc

# 장르 목록 순환 스레드
def run_genre_url_iterater(*args):
    arr_genre_url = args[0]
    for genre_url in arr_genre_url:
        get_video_list_links(genre_url)

# 장르 목록 페이지
def get_genre_list_page_links():
    max_thread = 1
    pydoc = get_pydoc('/en/genres.php')

    if pydoc == None:
        print("장르 목록 읽기 오류")
        return

    # 장르 리스트를 스레드만큼 나누어 담는다
    genre_url_hash = {}
    thread_idx = 0
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
            print("$$$$$$$$$$===================", genre_url, "=======================$$$$$$$$$$$$$$", genre_count)
            get_video_list_links(genre_url)
    #print("total genre count:", genre_count)

# 각 장르별 첫 페이지 목록. 여기서 마지막 페이징 번호를 얻을 수 있다.
# 샘플 url : vl_genre.php?g=da
def get_video_list_links(list_url):
    pydoc = get_pydoc(list_url)
    for i in range(1, 3):
        if pydoc != None:
            print("get url error to retry:", i)
            break
        else:
            pydoc = get_pydoc(list_url)

    attr = pydoc.find('.page.last').attr('href')
    if attr != None:
        arr_href = pydoc.find('.page.last').attr('href').split('=')
    else:
        log_error_url(list_url)
        return

    last_page = int(arr_href[-1])
    for i in reversed(range(2, last_page + 1)):
        url = '='.join(arr_href[0:-1]) + '=' + str(i)
        if redis.get("complete_video_list:" + url) != None:  # 완료된 리스트 페이지
            print("======================complete list=================:", url)
            continue
        pydoc = get_pydoc(url)
        if pydoc != None:
            get_video_from_list(pydoc)
        redis.set("complete_video_list:" + url, 1);
    get_video_from_list(pydoc)

# 비디오 정보 상세
def get_video_from_list(list_document):
    for video_element in list_document('.videos').find('.video'):
        url = get_sub_uri(pq(video_element).find('a').attr('href'))
        redis.set('last_url', url)
        if redis.get(url) != None: # 이미 해당 세션에서 방문한 적이 있음
            continue
        pydoc = get_pydoc(url)
        if pydoc != None:
            doc = ModelHelper(pydoc, url)
            doc.start_parse()

    ##POST EXAMPLE
    #url = 'http://was.smartcrm.kr/SmartCRM/webservice/xml_hosp.asp'
    #data = urlencode({ "chksum" : "23f07fae59a1a1eb160b145521269207" }).encode()
    #print(req.urlopen(url, data).read())

def start():
    if False:
        url = '/en/?v=javliolh3a'
        pydoc = pq(url=Config.d['proxy'] + Config.d['domain'] + url)
        doc = ModelHelper(pydoc, url)
        doc.start_parse()
    else:
        get_genre_list_page_links()
        #get_video_list_links('vl_genre.php?g=am')

def get_sub_uri(url):
    if url[:2] == './':
        return url[2:]

    if url[:4] == '/en/':
        return url

    return '/en/' + url

def check_valid_url(url):
    if url == None:
        return False

    if url.find("http") != -1 or url.find('www.') != -1:
        return False

    if url == './':
        return False

    if url == '.':
        return False

    return True

if __name__ == "__main__":
    start()