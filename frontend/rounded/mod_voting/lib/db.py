from rounded.core import redis

def _get_charities(db):
    doc_ref = redis.hgetall("charityVotes")
    return doc_ref

def get_charities(db):
    doc_ref = _get_charities(db)

    # processs dictionary
    charities = [
        {
            'name': key,
            'votes': int(doc_ref[key]),
            'description': "I don't feell like writing this",
        } for key in doc_ref 
    ]

    charities.sort(key=lambda x: x["votes"], reverse=True)
    return charities

def getTopCharity(db):
    charities = get_charities(db)

    if len(charities) == 0:
        return None
    return charities[0]

# increments number of votes charityName has
def increment_charity(db, charityName):
    redis.hincrby("charityVotes", charityName, 1)