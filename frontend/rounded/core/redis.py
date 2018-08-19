from flask import current_app as app
import redis

db = None

def init():
    global db
    url = app.config.get("REDIS_URL")
    if url == None:
        return
    db = redis.from_url(
        url,
        charset="utf-8", decode_responses=True
    )

def dbOperation(func):
    def _func(*argv, **kwargs):
        if db == None:
            init()
        if db == None:
            return None
        return func(*argv, **kwargs)
    _func.__name__ = func.__name__
    return _func

@dbOperation
def keys(pattern = None):
    return db.keys(pattern)

@dbOperation
def set(key, value):
    return db.set(key, value)

@dbOperation
def get(key):
    return db.get(key)

@dbOperation
def hget(key, field):
    return db.hget(key, field)

@dbOperation
def hset(key, field, value):
    return db.hset(key, field, value)

@dbOperation
def hgetall(key):
    return db.hgetall(key)

@dbOperation
def hincrby(key, field, amount = 1):
    return db.hincrby(key, field, amount)