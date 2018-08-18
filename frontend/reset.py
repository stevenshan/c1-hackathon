import rounded
import redis
import json

# setup app and request context
app = rounded.create_app()
ctx = app.test_request_context()
ctx.push()

# reset redis database
DATA = "rounded/core/charity_navigator/data.json"
data = json.load(open(DATA))
redisURL = app.config["REDIS_URL"]
redisDB = redis.from_url(redisURL)
redisDB.flushdb()

print("Writing charity info to redis DB: \n")
keys = list(data.keys())
for index, key in enumerate(keys):
    print(str(index) + "/" + str(len(keys)), end="\r")
    obj = data[key]
    name = obj["charityName"] 
    redisDB.hmset(name, obj)


