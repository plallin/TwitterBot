#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, os
import requests
import praw
from config import CONSUMER_KEY, SECRET_ACCESS_TOKEN, ACCESS_TOKEN, SECRET_CONSUMER_KEY

MAX_MESSAGE_LENGTH = 140

try:
    # Connect to Twitter
    print("Connect to Twitter--------------------------------------------------------------------------------", end=" ")
    auth = tweepy.OAuthHandler(CONSUMER_KEY, SECRET_CONSUMER_KEY)
    auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
    api = tweepy.API(auth)
    print("OK")

    # Get top post of the day
    print("Get top post--------------------------------------------------------------------------------------", end=" ")
    reddit = praw.Reddit('kittykittybot')
    subreddit = reddit.subreddit("catpictures")
    top_post = subreddit.top(limit=1, time_filter="day").next()
    post_title = top_post.title
    post_link = top_post.shortlink
    post_pic_url = top_post.url
    print("OK")

    # Download cat pic
    print("Download image------------------------------------------------------------------------------------", end=" ")
    kitten_pic = "kittykitty.jpg"
    req = requests.get(post_pic_url, stream=True)
    if req.status_code == 200:
        with open(kitten_pic, "wb") as img:
            for chunk in req:
                img.write(chunk)
    print("OK")

    # Prepare status update
    print("Set up status update------------------------------------------------------------------------------", end=" ")
    post_link_length = len(post_link)
    end_of_message = " - via " + post_link + " #Caturday"
    message_status = post_title + end_of_message

    if len(message_status) > MAX_MESSAGE_LENGTH:
        message_status = post_title[: MAX_MESSAGE_LENGTH - len(end_of_message) - 4] + "..." + end_of_message
    print("OK")

    # Post to Twitter
    print("Post to Twitter-----------------------------------------------------------------------------------", end=" ")
    api.update_with_media(kitten_pic, status=message_status)
    print("OK")

    #delete picture
    os.remove(kitten_pic)
except:
    print("FAIL")
    #api.update_status("@plallin OMG! I AM BREAKEN! PLZ FIX ")