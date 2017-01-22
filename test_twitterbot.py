import unittest
from bot import TwitterBot
from hypothesis import given
from hypothesis.strategies import text


class TwitterBotTest(unittest.TestCase):
    def test_upload_details(self):
        test_bot = TwitterBot("TestAccount", "config.json")
        test_bot.read_config_file()
        self.assertEqual(test_bot.ACCESS_TOKEN, "correct")
        self.assertEqual(test_bot.CONSUMER_KEY, "horse")
        self.assertEqual(test_bot.SECRET_ACCESS_TOKEN, "battery")
        self.assertEqual(test_bot.SECRET_CONSUMER_KEY, "staple")
        self.assertEqual(test_bot.hashtags, ["#wow", "#such", "#hashtag"])
        self.assertEqual(test_bot.error_message, "sample error message")

    @given(title=text(min_size=1, average_size=140), url=text(min_size=1, average_size=50))
    def test_status_length(self, title, url):
        test_bot = TwitterBot("TestAccount", "config.json")
        test_bot.reddit_post._title = title
        test_bot.reddit_post._url = url
        status_update = test_bot.status_update_message()
        self.assertTrue(len(status_update) <= 140)