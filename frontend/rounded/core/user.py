from flask import current_app as app
from rounded.core import redis

NAME = app.config.get("CUSTOMER")

def setCharity(charityName):
    print(redis.db)
    redis.set("user:" + str(NAME), charityName)

def getCharity():
    return redis.get("user:" + str(NAME))

