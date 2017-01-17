#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests
import praw
import json
import os
from PIL import Image
import logging
import sys
from config import ACCESS_TOKEN, SECRET_ACCESS_TOKEN, CONSUMER_KEY, SECRET_CONSUMER_KEY

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
    def update_rate(self):
        if not self._update_rate:
            self.read_config_file()
        return self._update_rate

    @property
    def hashtags(self):
        if not self._hashtags:
            self.read_config_file()
        return self._hashtags

    def error_message(self):
        if not self.error_message():
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
        self._subreddit = data["subreddit"]
        self._update_rate = data["update_rate"]
        self._hashtags = data["hashtags"]
        self._error_message = data["error_message"]

    def download_pic(self):
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
        self.download_pic()
        status_update = "I am writing sth"
        try:
            auth = tweepy.OAuthHandler(self._CONSUMER_KEY, self._SECRET_CONSUMER_KEY)
            auth.set_access_token(self._ACCESS_TOKEN, self._SECRET_ACCESS_TOKEN)
            api = tweepy.API(auth)
            print("status:", status_update)
            print("post title:", self.reddit_post.title)
            print("link:", self.reddit_post.url)
            print("pic link:", self.reddit_post.picture_url)
            api.update_with_media("AllThingsKute_pic.jpg", status="123")
        except tweepy.error.TweepError as err:
            print(type(err), err)
            logging.basicConfig(filename='error.log',
                                filemode='a',
                                level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
            logging.exception('\n\n******Error raised******')
        except Exception:
            logging.basicConfig(filename='other_error.log',
                                filemode='a',
                                level=logging.DEBUG,
                                format='%(asctime)s %(message)s')
            logging.exception('\n\nUnexpected error')


class RedditPost:
    def __init__(self, twitter_bot_name, config_file):
        self.config_file = config_file
        self.twitter_bot_name = twitter_bot_name
        self._subreddit = None
        self._client_id = None
        self._client_secret = None
        self._user_agent = None
        self._top_timeframe = None
        self._url = None
        self._title = None
        self._picture_url = None

    @property
    def subreddit(self):
        if not self._subreddit:
            self.read_config_file()
        return self._subreddit

    @property
    def client_id(self):
        if not self._client_id:
            self.read_config_file()
        return self._client_id

    @property
    def client_secret(self):
        if not self._client_secret:
            self.read_config_file()
        return self._client_secret

    @property
    def user_agent(self):
        if not self._user_agent:
            self.read_config_file()
        return self._user_agent

    @property
    def top_timeframe(self):
        if not self._top_timeframe:
            self.read_config_file()
        return self._top_timeframe

    @property
    def url(self):
        if not self._url:
            self.read_top_post()
        return self._url

    @property
    def title(self):
        if not self._title:
            self.read_top_post()
        return self._title

    @property
    def picture_url(self):
        if not self._picture_url:
            self.read_top_post()
            self.format_picture_url()
        return self._picture_url

    def read_config_file(self):
        with open(self.config_file) as data_file:
            data = json.load(data_file)
        data = data[self.twitter_bot_name]
        self._subreddit = data["subreddit"]
        self._client_id = data["reddit_client_id"]
        self._client_secret = data["reddit_client_secret"]
        self._user_agent = data["reddit_user_agent"]
        self._top_timeframe = data["update_rate"]

    def read_top_post(self):
        reddit = praw.Reddit(client_id=self.client_id,
                             client_secret=self.client_secret,
                             user_agent=self.user_agent)
        subreddit = reddit.subreddit(self.subreddit)
        all_top_posts = subreddit.top(limit=10, time_filter=self.top_timeframe)
        top_post = all_top_posts.next()
        while not ("imgur.com" in top_post.url or "reddituploads.com" in top_post.url):
            print(top_post.url)
            top_post = all_top_posts.next()
        self._title = top_post.title
        self._url = top_post.shortlink
        self._picture_url = top_post.url

    def format_picture_url(self):
        domain = self._picture_url[:self._picture_url.rfind("/")]
        path = self._picture_url[self._picture_url.rfind("/"):]
        extension = path.rfind(".")
        if extension < 0:
            self._picture_url += ".jpg"
        else:
            self._picture_url = domain + path[:extension] + ".jpg"


if __name__ == "__main__":
    botty_mcbotface = TwitterBot("AllThingsKute", "config.json")
    botty_mcbotface.post_to_twitter()
    print(botty_mcbotface.reddit_post.top_timeframe)
