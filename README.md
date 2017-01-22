![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)]

# Twitter Bot

A Twitter bot that scraps reddit and posts the top link featuring a picture from a given subreddit. The aim of the bot is to post a picture along with some text to Twitter on a regular basis.

# Bot example

See these 2 Twitter accounts for examples of what the bot does:

- [KittyKittyDaily](https://twitter.com/KittyKittyDaily) posts 1 message per day showing the daily top post from [/r/catpictures](https://www.reddit.com/r/catpictures)

- [AllThingsKute](https://twitter.com/AllThingsKute) posts 1 message per hour showing the hourly top post from [/r/aww](https://www.reddit.com/r/aww)

# Pre-requisite

You should have your own Twitter app and your own Reddit app. More information can be found on [the Twitter Platform](https://dev.twitter.com/) and on [the Reddit API documentation](https://www.reddit.com/dev/api/)

# Dependencies

The required libraries should be installed.

> cd /path/to/TwitterBot

> pip install -r requirements.txt

# Configuring the bot

The bot read `config.json` in order to be set up. This file should be created, and its formatting should be as follows:

<pre>
{
  "TwitterBotName": {
     "access_token": "your twitter app access token",
     "consumer_key": "your twitter app consumer key",
     "error_message": "an error message e.g.: @plallin I'm broken, please fix me!",
     "hashtags": [
       "#your",
       "#potential",
       "#hashtags",
       "#stored",
       "#in",
       "#an",
       "#array"
     ],
     "reddit_client_id": "your reddit app client id",
     "reddit_client_secret": "your reddit app secret client id",
     "reddit_user_agent": "your reddit user agent. By convention: AppName by /u/username",
     "secret_access_token": "Your twitter app secret access token",
     "secret_consumer_key": "Your twitter app secret consumer key",
     "subreddit": "the subreddit of interest",
     "update_rate": "the timeframe to retrieve the top post (hour/day/week/month/year/all"
   }
}
</pre>

If you are using more than 1 bot, just add its details to the same config file, as follows:

<pre>
{
  "TwitterBotName": {
     "access_token": "your twitter app access token",
     "consumer_key": "your twitter app consumer key",
     "error_message": "an error message e.g.: @plallin I'm broken, please fix me!",
     "hashtags": [
       "#your",
       "#potential",
       "#hashtags",
       "#stored",
       "#in",
       "#an",
       "#array"
     ],
     "reddit_client_id": "your reddit app client id",
     "reddit_client_secret": "your reddit app secret client id",
     "reddit_user_agent": "your reddit user agent. By convention: AppName by /u/username",
     "secret_access_token": "Your twitter app secret access token",
     "secret_consumer_key": "Your twitter app secret consumer key",
     "subreddit": "the subreddit of interest",
     "update_rate": "the timeframe to retrieve the top post (hour/day/week/month/year/all"
   }
  "OtherTwitterBotName": {
     "access_token": "your twitter app access token",
     "consumer_key": "your twitter app consumer key",
     "error_message": "an error message e.g.: @plallin I'm broken, please fix me!",
     "hashtags": [
       "#your",
       "#potential",
       "#hashtags",
       "#stored",
       "#in",
       "#an",
       "#array"
     ],
     "reddit_client_id": "your reddit app client id",
     "reddit_client_secret": "your reddit app secret client id",
     "reddit_user_agent": "your reddit user agent. By convention: AppName by /u/username",
     "secret_access_token": "Your twitter app secret access token",
     "secret_consumer_key": "Your twitter app secret consumer key",
     "subreddit": "the subreddit of interest",
     "update_rate": "the timeframe to retrieve the top post (hour/day/week/month/year/all"
   }
}
</pre>

# Using the bot

To use the bot, use the following command line:

> python bot.py TwitterBotName /path/to/config.json

# Scheduling Twitter updates

You may schedule a cron task to handle regular status updates of your Twitter bot (or your OS equivalent of a cron task).

See [CronHowTo](https://help.ubuntu.com/community/CronHowto) for an introduction to scheduling cron tasks.