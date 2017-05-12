import MySQLdb
import threading
import urllib.request as req
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from models.video import Video

valid_domain = 'www.javlibrary.com'
current_url = ''
touched_url = {}

#examples
#db = MySQLdb.connect(host="45.77.19.179", user="root", passwd="rntekrrntekr1!", port=4306)
#cursor = db.cursor()
#cursor.execute("INSERT INTO VALUES")
#cursor.execute("SELECT BLAH BLAH")
#cursor.fetchone()
#db.close()

def get_inside(url):
    if url in touched_url:
        return

    print("do touch:", url)

    current_url = url
    touched_url[url] = 1
    ##GET
    #doc = req.urlopen('http://45.77.19.179:1337/?url=http://www.goodoc.co.kr/events/5883?funnel=organic').read()
    #doc = pq(url='http://45.77.19.179:1337/?url=http://www.goodoc.co.kr/events/5883?funnel=organic')
    try:
        doc = pq(url='http://45.77.19.179:1337/?url=http://' + valid_domain + get_sub_uri(url))
        if url[:6] == '?v=jav':
            parse_doc(doc)
    except:
        print("Get URL Error:", url)
        return

    for a_element in doc('a'):
        url = pq(a_element).attr('href')
        is_valid_url = check_valid_url(url)
        if is_valid_url:
            get_inside(get_sub_uri(url))

    ##POST
    #url = 'http://was.smartcrm.kr/SmartCRM/webservice/xml_hosp.asp'
    #data = urlencode({ "chksum" : "23f07fae59a1a1eb160b145521269207" }).encode()
    #print(req.urlopen(url, data).read())

def list_genres(index, node):
    d = pq(node)
    print(d.attr('id'), d.text())

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

def parse_doc(doc):
    content_area = doc('#rightcolumn')
    print('title is:', content_area('#video_title').text())
    jacket_info = content_area('#video_jacket_info')
    print('video id is:', jacket_info('#video_id').text())
    print('jacket image url:', jacket_info('#video_jacket_img').attr('src'))
    print('release date:', jacket_info('#video_date').find('text').text())
    print('video_length:', jacket_info('#video_length').find('.text').text())
    print('director:', jacket_info('#video_director').find('.director').text())
    print('maker:', jacket_info('#video_maker').find('.maker').text())
    print('label:', jacket_info('#video_label').find('.label').text())
    print('genres')
    jacket_info('#video_genres').find('.genre').each(list_genres)
    print('cast')
    jacket_info('#video_cast').find('.cast').each(list_cast)
    print('comments')
    content_area('#video_comments').find('.comment').each(list_comment)

def func(*args):
    #get_inside('/en/')
    #get_inside('/en/#help_topic1')
    #doc = pq(url='http://45.77.19.179:1337/?url=http://www.javlibrary.com/en/?v=javlikic6e')
    #doc = pq(url='http://45.77.19.179:1337/?url=http://www.javlibrary.com/en/?v=javliki22u')
    #parse_doc(doc)
    print("what the?")

thread = threading.Thread(target=func, args=(1, 2))
thread.start()
#thread.join()

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

    if url == current_url:
        return False

    if url == './':
        return False

    if url == '.':
        return False

    return True