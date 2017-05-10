import threading
import urllib.request as req
from urllib.parse import urlencode
from pyquery import PyQuery as pq

valid_domain = 'www.javlibrary.com'
current_url = ''
touched_url = {}

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
        doc = pq(url='http://45.77.19.179:1337/?url=http://' + valid_domain + url)
    except:
        print("Get URL Error:", url)
        return

    for a_element in doc('a'):
        url = pq(a_element).attr('href')
        is_valid_url = check_valid_url(url)
        if is_valid_url:
            get_inside(strip_url(url))

    ##POST
    #url = 'http://was.smartcrm.kr/SmartCRM/webservice/xml_hosp.asp'
    #data = urlencode({ "chksum" : "23f07fae59a1a1eb160b145521269207" }).encode()
    #print(req.urlopen(url, data).read())

def func(*args):
    get_inside('/en/')

thread = threading.Thread(target=func, args=(1, 2))
thread.start()
#thread.join()

def strip_url(url):
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