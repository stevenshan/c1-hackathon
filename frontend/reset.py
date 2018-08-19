import rounded
import redis
import json
import random

# setup app and request context
app = rounded.create_app()
ctx = app.test_request_context()
ctx.push()

# reset redis database
DATA = "charity_data.json"
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


