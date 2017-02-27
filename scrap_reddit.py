#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import praw


class RedditPost:

    """A class to scrap reddit.
    It retrieves the top post of a given timeframe and its associated title and links.

    Attributes:
        twitter_bot_name: the name of the associated twitter bot
        config_file: path the the config file
    """

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
        self._picture_extension = None

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
            self.fetch_content()
        return self._url

    @property
    def title(self):
        if not self._title:
            self.fetch_content()
        return self._title

    @property
    def picture_url(self):
        if not self._picture_url:
            self.fetch_content()
            self.format_picture_url()
        return self._picture_url

    @property
    def picture_extension(self):
        if not self._picture_extension:
            self.fetch_content()
        return self._picture_extension

    def read_config_file(self):
        """Read the config file in order to get the attributes:
            _subreddit: the subreddit to be scrapped
            _client_id: the client id to access reddit
            _client_secret: the secret client id to access reddit
            _user_agent: the user agent to access reddit
            _top_timeframe: the timeframe which should be used to retrieve the top post
        """
        with open(self.config_file) as data_file:
            data = json.load(data_file)
        data = data[self.twitter_bot_name]
        self._subreddit = data["subreddit"]
        self._client_id = data["reddit_client_id"]
        self._client_secret = data["reddit_client_secret"]
        self._user_agent = data["reddit_user_agent"]
        self._top_timeframe = data["update_rate"]

    def fetch_content(self):
        """Read top post for a given timeframe, for the subreddit as input in the config file.
        It updates the bot attributes:
            _title: the title of the top post
            _url: the link to the post post (shortlink)
            _picture_url: the link to the picture referenced by the top post

        In case the top post is not a picture, it will get the next best top post, until a picture is found.
        Pictures are detected using their link (imgur.com or redditupload.com)
        """
        reddit = praw.Reddit(client_id=self.client_id,
                             client_secret=self.client_secret,
                             user_agent=self.user_agent)
        subreddit = reddit.subreddit(self.subreddit)
        all_top_posts = subreddit.top(limit=100, time_filter=self.top_timeframe)
        top_post = None  # initialising the variable
        extension = -1
        while extension == -1:
            top_post = all_top_posts.next()
            path = top_post.url[top_post.url.rfind("/"):]  # find the path to the media content
            extension = path.rfind(".")  # find the media extension
        self._title = top_post.title
        self._url = top_post.shortlink
        self._picture_url = top_post.url
        self._picture_extension = path[extension:] if path[extension:].lower() != ".gifv" else ".mp4"
        if self._picture_url[-5:].lower() == ".gifv":
            self._picture_url = self._picture_url[:-5] + ".mp4"  # a url pointing to a gifv can't be properly downloaded

