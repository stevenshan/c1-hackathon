def _get_charities(db):
    doc_ref = db.collection(u'charityOfTheWeek').document(u'charityVotes').get().to_dict()
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

def increment(db, charityUpdate):
    data = charityUpdate
    print(">>" + str(data))
    #db.collection(u'users').document(u'{:}'.format(user)).document(u'suggestion').set(data)
    user_ref = db.collection(u'charityOfTheWeek').document(u'charityVotes')
    user_ref.update(data)

# finds top suggestion and pushes to database
def increment_charity(db, charityName):
    charities = _get_charities(db)
    updatedCharity = charities[charityName] + 1
    charities[charityName] = updatedCharity
    increment(db, charities)