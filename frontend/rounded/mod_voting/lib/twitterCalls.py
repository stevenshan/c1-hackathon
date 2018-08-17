import tweepy

cfg = {
  "consumer_key"        : "YTjzYW8UDRUTNbStu2vSoOunv",
  "consumer_secret"     : "3laraBw3oyMbqIt8RdAm281kKW4OpHukRSx90vXweFbM9ylvwN",
  "access_token"        : "1030182022176796672-xpry2rloo4AxJdYMNnjlkLYiboafPY",
  "access_token_secret" : "293ToO4YQDYERqQgSiNZLPB756IvBPoTlrmMb4c7t1eaC"
}

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def tweetVoteMessage(charityName):
  tweet = "Hey, I voted to donate to " + charityName + "! You can donate with Capital One ROUNDED too!"
  api = get_api(cfg)
  status = api.update_status(status=tweet)
