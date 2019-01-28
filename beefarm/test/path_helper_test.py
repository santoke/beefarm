from app.path_helper import PathHelper
from app.config import Config
import unittest

class PathHelperTest(unittest.TestCase):
    def test_runs(self):
        Config()

        language = Config.d['language']
        t = PathHelper(language)

        # 하위 경로 언어 붙여서 가져오기
        self.assertEqual(t.make_sub_path(f'/{language}/documents'), f'/{language}/documents')
        self.assertEqual(t.make_sub_path('./documents'), 'documents')
        self.assertEqual(t.make_sub_path('documents/'), f'/{language}/documents/')

        # 프록시 주소가 붙는 경로
        url = 'documents'
        expected = Config.d['proxy'] + Config.d['domain'] + f'/{language}/{url}'
        self.assertEqual(t.page_url(url), expected)