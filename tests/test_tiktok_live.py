import unittest
from api.tiktok_live import TikTokLiveHandler

class TestTikTokLiveHandler(unittest.TestCase):
    def test_initialization(self):
        handler = TikTokLiveHandler("username")
        self.assertEqual(handler.username, "username")
        self.assertIsNotNone(handler.client)

if __name__ == "__main__":
    unittest.main()
