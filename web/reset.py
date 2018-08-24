'''
loads information in redis database and makes sure nessie capital one api is setup
'''

import rounded
import redis
import json
import random
import time

# setup app and request context
app = rounded.create_app()
ctx = app.test_request_context()
ctx.push()

from flask import current_app as app
from rounded.core.user_info import accounts

print("Creating accounts")
accounts.reset_accounts()
accounts.add_checking_account()
accounts.add_charity_account()
print("Done. Quit now if that's all you wanted.")

time.sleep(5)

# reset redis database
DATA = "data/charity_data.json"
data = json.load(open(DATA))
redisURL = app.config["REDIS_URL"]
redisDB = redis.from_url(redisURL)
redisDB.flushdb()

print("Writing charity info to redis DB: ")
keys = list(data.keys())
ids = {}
for index, key in enumerate(keys):
    print(str(index) + "/" + str(len(keys)), end="\r")
    obj = data[key]
    name = obj["charityName"] 
    obj["key"] = key
    redisDB.hmset("charity:" + name, obj)
    ids[key] = "charity:" + name

    # randomly add to voting system
    rand = random.random()
    if rand < 0.0066666:
        redisDB.hset("charityVotes", name, 0)

redisDB.hmset("idMap", ids)

print("\n\n")


