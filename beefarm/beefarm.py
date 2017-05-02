import threading
import urllib.request as req
from urllib.parse import urlencode
from pyquery import PyQuery as pq

def func(*args):
    #proxy = req.ProxyHandler({'http': r'http://chocho:goodocgoodoc@45.77.19.179:6974'})
    #proxy = req.ProxyHandler({})
    #auth = req.HTTPBasicAuthHandler()
    #opener = req.build_opener(proxy, auth, req.HTTPHandler)
    #req.install_opener(opener)


    ##GET
    #doc = req.urlopen('http://45.77.19.179:1337/?url=http://www.goodoc.co.kr/events/5883?funnel=organic').read()
    #doc = pq(url='http://45.77.19.179:1337/?url=http://www.goodoc.co.kr/events/5883?funnel=organic')
    doc = pq(url='http://45.77.19.179:1337/?url=http://www.javlibrary.com/en')
    for a_element in doc('a'):
        print(pq(a_element).attr('href'))

    ##POST
    #url = 'http://was.smartcrm.kr/SmartCRM/webservice/xml_hosp.asp'
    #data = urlencode({ "chksum" : "23f07fae59a1a1eb160b145521269207" }).encode()
    #print(req.urlopen(url, data).read())

thread = threading.Thread(target=func, args=(1, 2))
thread.start()
#thread.join()