from app.config import Config
from app.video_page import VideoPage
from pyquery import PyQuery as pq

import unittest

class VideoPageTest(unittest.TestCase):
    def setUp(self):
        Config()
        self.v = VideoPage('?v=javli7r65y')

    def test_runs(self):
        self.assertEqual(True, True)

    def test_set_video_id(self):
        self.v.set_video_id()
        self.assertEqual(self.v.video_id, 'NSPS-773')

    def test_get_id_and_name(self):
        test_id = 'my_id'
        test_text = '기도허냐'
        id, text = self.v.get_id_and_name(pq(f'<div id="{test_id}">{test_text}</div>'))
        self.assertEqual(id, test_id)
        self.assertEqual(text, test_text)