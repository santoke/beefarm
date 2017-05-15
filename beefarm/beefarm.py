import urllib.request as req
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from app.document import Document
from app.config import Config

Config()

touched_url = {}

def get_links(url, referer, use_reflextion=True):
    if url in touched_url:
        return

    print("do touch refer:", referer, ", to :", url)

    touched_url[url] = 1

    try:
        pydoc = pq(url=Config.d['proxy'] + Config.d['domain'] + get_sub_uri(url))
        print(pydoc)
        if url[:6] == '?v=jav':
            doc = Document(pydoc, url)
            doc.start_parse()
    except Exception as ex:
        print("Get URL Error:", url, ex)
        return

    for a_element in pydoc('a'):
        a_url = pq(a_element).attr('href')
        if use_reflextion == False:
            print(a_url)
        is_valid_url = check_valid_url(a_url)
        if is_valid_url and use_reflextion:
            get_links(get_sub_uri(a_url), a_url)

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
        get_links('/en/vl_newrelease.php', '', True)
        #get_links('/en/vl_genre.php?list&mode=&g=ky&page=1', '', True)

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