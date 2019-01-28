from test.test_main import TestMain
from app.config import Config
from app.document import Document

Config()

def start():
    if True: # 디버깅 모드로 테스트 모듈 진입
        # 셀레늄으로 쿠키 가져오기 예제
        #driver = webdriver.Chrome()
        #url = Config.d['domain'] + '/' + Config.d['language'] + '/'
        #driver.get(url)
        #all_cookies = driver.get_cookies()
        #print(all_cookies)

        d = Document()
        #genres = d.get_genre_list_page_links()
        last_link = d.get_video_last_paging_links('vl_genre.php?g=da')
        print(last_link)
    else:
        get_genre_list_page_links()
        #get_video_list_links('vl_genre.php?g=am')

if __name__ == "__main__":
    start()