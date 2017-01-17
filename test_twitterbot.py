import unittest
from bot import TwitterBot

class TwitterBotTest(unittest.TestCase):

    def test_upload_details(self):
        test_bot = TwitterBot("TestAccount", "config.json")
        test_bot.read_config_file()
        self.assertEqual(test_bot.ACCESS_TOKEN, "correct")
        self.assertEqual(test_bot.CONSUMER_KEY, "horse")
        self.assertEqual(test_bot.SECRET_ACCESS_TOKEN, "battery")
        self.assertEqual(test_bot.SECRET_CONSUMER_KEY, "staple")
        self.assertEqual(test_bot.update_rate, "hour")
        self.assertEqual(test_bot.hashtags, ["#wow", "#such","#hashtag"])
        self.assertEqual(test_bot.error_message, "sample error message")