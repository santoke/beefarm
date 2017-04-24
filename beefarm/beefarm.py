import threading
import urllib.request

def func(*args):
    #thread process is here
    print(urllib.request.urlopen("http://www.google.co.kr").read())

thread = threading.Thread(target=func, args=(1, 2))
thread.start()
#thread.join()