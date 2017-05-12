import urllib.request as req
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from app.document import Document

valid_domain = 'www.javlibrary.com'
current_url = ''
touched_url = {}

# SELECT
#queries = db_session.query(Video)
#entries = [dict(id='TESTD1111', length=100) for q in queries]
#print(entries)
#video = db_session.query(Video).filter_by(id='TESTD1111').first()

#UPDATE
#video = db_session.query(Video).filter_by(id='TESTD1111').first()
#video.subject = 'edited subject2222'
#db_session.commit()

# INSERT
#v = Video('TESTD11112', 'wowowo..', 'http://ssss.sss.com', '2017-07-12', 100)
#db_session.add(v)
#db_session.commit()
#print("v id is:", v.id)

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
            #thread = threading.Thread(target=parse_doc, doc=doc)
            #thread.start()
            print("hehehehe")
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

def start():
    #get_inside('/en/')
    #get_inside('/en/#help_topic1')
    #doc = pq(url='http://45.77.19.179:1337/?url=http://www.javlibrary.com/en/?v=javlikic6e')
    pydoc = pq(url='http://45.77.19.179:1337/?url=http://www.javlibrary.com/en/?v=javlikidyi')
    #thread = threading.Thread(target=parse_doc, args=(doc, 2))
    #thread.start()
    #print("what the?")
    doc = Document(pydoc)
    doc.start_parse()

#def func(*args):
#    parse_doc(args[0])

#thread = threading.Thread(target=func, args=(1, 2))
#thread.start()
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

start()