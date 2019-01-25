import unittest
from app.config import Config

class TestMain(unittest.TestCase):
    def test_runs(self):
        Config()
        print('누가 크래시 소리를 내었는가')

if __name__ == '__main__':
    unittest.main()