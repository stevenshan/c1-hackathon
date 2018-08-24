import tweepy
from flask import current_app as app

cfg = app.config.get("TWITTER")

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def tweetVoteMessage(charityName):
  tweet = "Hey, I voted to donate to " + charityName + "! You can donate with Capital One ROUNDED too!"
  api = get_api(cfg)
  status = api.update_status(status=tweet)
