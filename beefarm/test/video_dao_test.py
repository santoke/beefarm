from app.config import Config
from database import Connection
from app.video_dao import VideoDAO

import unittest

class VideoDAOTest(unittest.TestCase):

    def setUp(self):
        Config()
        Connection()
        self.v = VideoDAO()

    def test_get_video(self):
        self.v.get_video('NSPS-773')