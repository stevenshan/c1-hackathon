import tweepy

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main():
  cfg = {
    "consumer_key"        : "YTjzYW8UDRUTNbStu2vSoOunv",
    "consumer_secret"     : "3laraBw3oyMbqIt8RdAm281kKW4OpHukRSx90vXweFbM9ylvwN",
    "access_token"        : "1030182022176796672-xpry2rloo4AxJdYMNnjlkLYiboafPY",
    "access_token_secret" : "293ToO4YQDYERqQgSiNZLPB756IvBPoTlrmMb4c7t1eaC"
    }

  api = get_api(cfg)
  tweet = "@Valentino_JD is having fun at Cap1SES!!!"
  status = api.update_status(status=tweet)

if __name__ == "__main__":
  main()
