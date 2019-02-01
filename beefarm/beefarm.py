from test.test_main import TestMain
from app.config import Config
from app.document import Document

import sys

# 디버깅 모드로 테스트
def test():
    d = Document()
    genres = d.get_genre_list_page_links()
    last_link = d.get_last_paging_link('vl_genre.php?g=da')
    #d.iterate_paging(last_link)
    print(genres, last_link)

def start():
    d = Document()
    arr_genres = d.get_genre_list_page_links()
    for genre in arr_genres:
        last_page = d.get_last_paging_link(genre)
        #d.iterate_paging(last_page)

if __name__ == "__main__":
    Config()

    if len(sys.argv) > 1 and sys.argv[1] == '1':
        test()
    else:
        start()