import unittest
from bot import RedditPost


class RedditPostTest(unittest.TestCase):

    def test_format_url_gif(self):
        reddit_post = RedditPost("", "")
        reddit_post._picture_url = "https://i.imgur.com/6u8CtM9.gif"
        reddit_post.format_picture_url()
        self.assertEqual(reddit_post.picture_url, "https://i.imgur.com/6u8CtM9.jpg")

    def test_format_url_gifv(self):
        reddit_post = RedditPost("", "")
        reddit_post._picture_url = "https://i.imgur.com/QTCeiNM.gifv"
        reddit_post.format_picture_url()
        self.assertEqual(reddit_post.picture_url, "https://i.imgur.com/QTCeiNM.jpg")

    def test_format_url_noextension(self):
        reddit_post = RedditPost("", "")
        reddit_post._picture_url = "https://i.reddituploads.com/f560a6cffcf548b78bf19a0939dedb7d?fit=max&h=1536&w=1536&s=61ec3badb3792e8af49c17c143bf78e7"
        reddit_post.format_picture_url()
        self.assertEqual(reddit_post.picture_url, "https://i.reddituploads.com/f560a6cffcf548b78bf19a0939dedb7d?fit=max&h=1536&w=1536&s=61ec3badb3792e8af49c17c143bf78e7.jpg")