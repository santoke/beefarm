from app.uri_helper import URIHelper
from app.config import Config
import unittest

class URIHelperTest(unittest.TestCase):
    def test_runs(self):
        language = 'en'
        t = URIHelper(language)

        self.assertEqual(t.make_sub_uri(f'/{language}/documents'), f'/{language}/documents')
        self.assertEqual(t.make_sub_uri('./documents'), 'documents')
        self.assertEqual(t.make_sub_uri('documents/'), f'/{language}/documents/')

        url = 'documents'
        expected = Config.d['proxy'] + Config.d['domain'] + f'/{language}/{url}'
        self.assertEqual(t.page_url(url), expected)