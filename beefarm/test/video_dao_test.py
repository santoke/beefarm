from app.config import Config
from database import Connection
from app.video_dao import VideoDAO

from models.video import Video

import unittest

class VideoDAOTest(unittest.TestCase):

    def setUp(self):
        Config()

        self.v = VideoDAO()
        self.test_id = 'TEST-123'

        self.v.session.add(Video(self.test_id))
        self.v.commit()

    def test_get_video(self):
        video = self.v.get_video(self.test_id)
        self.assertEqual(video.id, self.test_id)

    def test_add_if_not_exist(self):
        # case 1. 데이터가 이미 존재함
        video = self.v.add_if_not_exist(self.test_id)
        self.v.commit()

        self.assertEqual(video.id, self.test_id)

        # case 2. 데이터가 없어서 새로 생성해야 할 경우
        self.v.session.delete(video)
        self.v.commit()
        video = self.v.add_if_not_exist(self.test_id)
        self.v.commit()

        self.assertEqual(video.id, self.test_id)

    def tearDown(self):
        test_video = Video.query.filter_by(id=self.test_id).first()
        if test_video:
            self.v.session.delete(test_video)
        self.v.commit()