from test.test_main import TestMain
from app.config import Config
from app.document import Document

Config()

# 디버깅 모드로 테스트
def test():
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

def start():
    d = Document()
    arr_genres = d.get_genre_list_page_links()
    for genre in arr_genres:
        last_page = d.get_video_last_paging_links(genre)
        d.iterate_paging(last_page)

if __name__ == "__main__":
    test()
    #start()