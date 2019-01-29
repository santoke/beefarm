import unittest
import re
from unittest import mock
from unittest.mock import patch
from app.config import Config
from app.document import Document

class DocumentTest(unittest.TestCase):
    def setUp(self):
        # todo : setup redis keys for test
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
    def test_get_last_paging_links(self):
        genre_url = 'vl_genre.php?g=da'
        category = genre_url.split('=')[1]
        last_page = self.document.get_last_paging_links(genre_url)
        p = re.compile(f'vl_genre.php\?&mode=&g={category}&page=[0-9]')
        self.assertNotEquals(p.search(last_page), None)

    # 페이징 순환
    @patch.object(Document, 'get_video_detail')
    def test_iterate_paging(self, mock_get):
        mock_get_video_detail = self._mock_get_video_detail()
        mock_get.return_value = mock_get_video_detail

        last_page = 5
        url = '/en/vl_genre.php?&mode=&g=da'
        last_url = f'{url}&page={last_page}'
        arr_href = last_url.split('=')

        cache_page_start = 3
        self.document.iterate_paging(last_url, cache_page_start)
        for i in range(cache_page_start, last_page + 1):
            lurl = f'{url}&page={i}'
            redis_key = f'complete_video_list:{lurl}'
            self.assertNotEquals(self.document.redis.get(redis_key), None)

    def test_get_video_detail(self):
        print('this is test video detail')

    # 비디오 상세 목업
    def _mock_get_video_detail(self, list_html='', force_raise=None):
        mock_response = mock.Mock()
        if force_raise:
            mock_response.raise_for_status.side_effect = force_raise

    def tearDown(self):
        # todo, remove tested redis keys
        print('Document Test End')