#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys

argfile = str(sys.argv[1])

# enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'M0KJwJ9rXdu4Rr6IbQtuYJ8uC'  # keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'KWKDkv7sRTyFZi1TafkzASRhglxklD3du0mh6U1Qt6poIKWfUG'  # keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '159480948-Tr3QBQH0l6DIKL6gsrqvCHKzZsytw4Fu2FpbouEP'  # keep the quotes, replace this with your access token
ACCESS_SECRET = '82y9Dwwrf03aN5DVgIEKHPvcbBVaK1HKHNCNCVCfEiERm'  # keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

filename = open(argfile, 'r')
f = filename.readlines()
filename.close()

for line in f:
    api.update_status(line)
    time.sleep(900)  # Tweet every 15 minutes
