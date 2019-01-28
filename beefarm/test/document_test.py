import unittest
import re
from app.config import Config
from app.document import Document

class DocumentTest(unittest.TestCase):
    def setUp(self):
        Config()
        self.document = Document()

    def test_runs(self):
        pydoc = self.document.pydoc('/en/')
        self.assertNotEquals(pydoc, None)

    # 장르 목록
    def test_get_genre_list(self):
        genre_urls = self.document.get_genre_list_page_links()
        check_string = 'vl_genre.php?'
        for url in genre_urls:
            self.assertEqual(url[0:len(check_string)], check_string)

    # 특정 장르의 마지막 페이징 번호
    def test_get_video_last_paging_links(self):
        genre_url = 'vl_genre.php?g=da'
        category = genre_url.split('=')[1]
        last_page = self.document.get_video_last_paging_links(genre_url)
        p = re.compile(f'vl_genre.php\?&mode=&g={category}&page=[0-9]')
        self.assertNotEquals(p.search(last_page), None)

    def tearDown(self):
        print('Document Test End')