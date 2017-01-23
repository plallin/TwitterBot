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

    @given(title=text(min_size=1, average_size=140))
    def test_status_length(self, title):
        test_bot = TwitterBot("TestAccount", "config.json")
        test_bot.reddit_post._title = title
        test_bot.reddit_post._url = "a" * 23  # Twitter URL are always 23 characters long
        status_update = test_bot.define_status_update()
        self.assertTrue(len(status_update) <= 140)

    def test_status_accuracy_short(self):
        test_bot = TwitterBot("TestAccount", "config.json")
        test_bot.reddit_post._title = "This is a short title"
        test_bot.reddit_post._url = "http://www.example.com/"
        status_update = test_bot.define_status_update()
        self.assertEqual(status_update, "This is a short title #wow #such #hashtag via http://www.example.com/")

    def test_status_accuracy_long(self):
        test_bot = TwitterBot("TestAccount", "config.json")
        test_bot.reddit_post._title = "This is a very, very long title which is well over 140 characters! Obviously, since Twitter only allows a maximum of 140 characters per message, it should be truncated."
        test_bot.reddit_post._url = "http://www.example.com/"
        status_update = test_bot.define_status_update()
        self.assertEqual(status_update,
                         "This is a very, very long title which is well over 140 characters! Obviously, since Twitter only allows a max... via http://www.example.com/")