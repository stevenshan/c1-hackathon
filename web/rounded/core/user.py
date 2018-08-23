from flask import current_app as app
from rounded.core import redis

NAME = app.config.get("CUSTOMER")

def setCharity(charityName):
    redis.hset("user:" + str(NAME), "charity", charityName)

def getCharity():
    return redis.hget("user:" + str(NAME), "charity")

