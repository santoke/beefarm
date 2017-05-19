import urllib.request as req
import redis
import threading
import time
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from app.document import Document
from app.config import Config
from database import db_session
from models.url import Url
from models.error_url import ErrorUrl

Config()
redis = redis.StrictRedis(host='localhost', port=6379, db=0)
redis.flushdb()
last_touch_url = '';

def log_site_url(url):
    redis.set(url, 1)
    if db_session.query(Url).filter_by(url=url).first() == None:
        db_session.add(Url(url))
        db_session.commit()

def get_pydoc(url):
    url = Config.d['proxy'] + Config.d['domain'] + get_sub_uri(url)
    print("to get pydoc:", url)
    log_site_url(url)
    try:
        pydoc = pq(url=url)
    except Exception as ex:
        if db_session.query(ErrorUrl).filter_by(url=url).first() == None:
            db_session.add(ErrorUrl(url))
            db_session.commit()
            print("Get URL Error:", url, ex)
            return None
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
        #thread = threading.Thread(target=run_genre_url_iterater, args=(genre_url_hash[hash_key], 1))
        #thread.start()
        for genre_url in genre_url_hash[hash_key]:
            genre_count = genre_count + 1
            print(genre_url, genre_count)
            get_video_list_links(genre_url)
    #print("total genre count:", genre_count)

# 각 장르별 첫 페이지 목록. 여기서 마지막 페이징 번호를 얻을 수 있다.
# 샘플 url : vl_genre.php?g=da
def get_video_list_links(list_url):
    pydoc = get_pydoc(list_url)
    arr_href = pydoc.find('.page.last').attr('href').split('=')
    last_page = int(arr_href[-1])
    get_video_from_list(pydoc)
    for i in range(2, last_page):
        url = '='.join(arr_href[0:-1]) + '=' + str(i)
        pydoc = get_pydoc(url)
        if pydoc != None:
            get_video_from_list(pydoc)

# 비디오 정보 상세
def get_video_from_list(list_document):
    for video_element in list_document('.videos').find('.video'):
        url = get_sub_uri(pq(video_element).find('a').attr('href'))
        if redis.get(url) != None: # 이미 해당 세션에서 방문한 적이 있음
            continue
        pydoc = get_pydoc(url)
        if pydoc != None:
            doc = Document(pydoc, url)
            doc.start_parse()


####
def start_get_link_thread(*args):
    get_links(args[0], args[1], True, args[2])

def get_links(url, referer, use_reflextion, depth=1):
    print("do touch refer:", referer, ", to :", url, "depth:", depth)
    last_touch_url = url;

    if depth == 5:
        return

    if use_reflextion and redis.get(url) != None:
        return

    if use_reflextion:
        redis.set(url, 1)
        if db_session.query(Url).filter_by(url=url).first() == None:
            db_session.add(Url(url))
            db_session.commit()
        else:
            if referer != '': # referr가 존재하고 이미 해당 DB를 읽은적이 있음
                return
    try:
        pydoc = pq(url=Config.d['proxy'] + Config.d['domain'] + get_sub_uri(url))
        # get documents
        if url.find('?v=jav') != -1:
            doc = Document(pydoc, url)
            doc.start_parse()
    except Exception as ex:
        if db_session.query(ErrorUrl).filter_by(url=url).first() == None:
            db_session.add(ErrorUrl(url))
            db_session.commit()
        print("Get URL Error:", url, ex)
        return

    for a_element in pydoc('a'):
        a_url = pq(a_element).attr('href')
        if use_reflextion == False:
            print(a_url)
        print(a_url)
        is_valid_url = check_valid_url(a_url)
        if is_valid_url and use_reflextion:
            #thread = threading.Thread(target=start_get_link_thread, args=(a_url, url, depth + 1))
            #thread.start()
            get_links(get_sub_uri(a_url), url, True, depth+1)

    ##GET EXAMPLE
    #doc = req.urlopen('http://45.77.19.179:1337/?url=http://www.goodoc.co.kr/events/5883?funnel=organic').read()

    ##POST EXAMPLE
    #url = 'http://was.smartcrm.kr/SmartCRM/webservice/xml_hosp.asp'
    #data = urlencode({ "chksum" : "23f07fae59a1a1eb160b145521269207" }).encode()
    #print(req.urlopen(url, data).read())

def start():
    if False:
        url = '/en/?v=javlikic6e'
        pydoc = pq(url=Config.d['proxy'] + Config.d['domain'] + url)
        doc = Document(pydoc, url)
        doc.start_parse()
    else:
        #get_links('/en/vl_newrelease.php', '', True)
        #get_links('/en/vl_genre.php?list&mode=&g=ky&page=1', '', True) # error when get with proxy
        #get_genre_list_page_links();
        #get_video_list_links('vl_genre.php?g=da');
        get_genre_list_page_links()

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