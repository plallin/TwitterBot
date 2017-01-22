#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests
import json
import os
from PIL import Image
import logging
import sys
from scrap_reddit import RedditPost

logging.basicConfig(filename='unexpected_error.log',
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')


class TwitterBot:
    MAX_MESSAGE_LENGTH = 140
    MAX_IMAGE_SIZE_BYTES = 3072000

    def __init__(self, twitter_account, config_file):
        self.twitter_account = twitter_account
        self.reddit_post = RedditPost(twitter_account, config_file)
        self.config_file = config_file
        self.picture = twitter_account + "_pic.jpg"
        self._CONSUMER_KEY = None
        self._SECRET_CONSUMER_KEY = None
        self._ACCESS_TOKEN = None
        self._SECRET_ACCESS_TOKEN = None
        self._hashtags = None
        self._error_message = None

    @property
    def CONSUMER_KEY(self):
        if not self._CONSUMER_KEY:
            self.read_config_file()
        return self._CONSUMER_KEY

    @property
    def SECRET_CONSUMER_KEY(self):
        if not self._SECRET_CONSUMER_KEY:
            self.read_config_file()
        return self._SECRET_CONSUMER_KEY

    @property
    def ACCESS_TOKEN(self):
        if not self._ACCESS_TOKEN:
            self.read_config_file()
        return self._ACCESS_TOKEN

    @property
    def SECRET_ACCESS_TOKEN(self):
        if not self._SECRET_ACCESS_TOKEN:
            self.read_config_file()
        return self._SECRET_ACCESS_TOKEN

    @property
    def hashtags(self):
        if not self._hashtags:
            self.read_config_file()
        return self._hashtags

    @property
    def error_message(self):
        if not self._error_message:
            self.read_config_file()
        return self._error_message

    def read_config_file(self):
        with open(self.config_file) as data_file:
            data = json.load(data_file)

        data = data[self.twitter_account]
        self._CONSUMER_KEY = data["consumer_key"]
        self._SECRET_CONSUMER_KEY = data["secret_consumer_key"]
        self._ACCESS_TOKEN = data["access_token"]
        self._SECRET_ACCESS_TOKEN = data["secret_access_token"]
        self._hashtags = data["hashtags"]
        self._error_message = data["error_message"]

    def download_picture(self):
        req = requests.get(self.reddit_post.picture_url, stream=True)
        if req.status_code == 200:
            with open(self.picture, "wb") as img:
                for chunk in req:
                    img.write(chunk)
        while os.stat(self.picture).st_size > type(self).MAX_IMAGE_SIZE_BYTES:
            self.resize_picture()

    def resize_picture(self):
        picture = Image.open(self.picture).convert('RGB')
        picture = picture.resize((picture.size[0] // 2, picture.size[1] // 2), Image.ANTIALIAS)
        picture.save(self.picture, optimize=True, quality=85)

    def status_update_message(self):
        message = self.reddit_post.title
        link = " via " + self.reddit_post.url
        if len(message + link) > 140:
            message = message[:140 - len(link) - 3] + "..."
        else:
            i = 0
            while i < len(self.hashtags) and len(message + " " + self.hashtags[i] + link) < type(self).MAX_MESSAGE_LENGTH:
                message += " " + self.hashtags[i]
                i += 1
        return message + link

    def post_to_twitter(self):
        self.download_picture()
        status_update = self.status_update_message()
        try:
            auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.SECRET_CONSUMER_KEY)
            auth.set_access_token(self.ACCESS_TOKEN, self.SECRET_ACCESS_TOKEN)
            api = tweepy.API(auth)
            api.update_with_media(self.picture, status=status_update)
            os.remove(self.picture)
        except tweepy.error.TweepError as err:
            print(type(err), err)
            logging.exception('\n\n******Error raised******')
            logging.error("status update:", status_update)
        except Exception as err:
            print(type(err), err)
            logging.exception('\n\nUnexpected error')


if __name__ == "__main__":
    botty_mcbotface = TwitterBot(sys.argv[1], sys.argv[2])
    botty_mcbotface.post_to_twitter()
