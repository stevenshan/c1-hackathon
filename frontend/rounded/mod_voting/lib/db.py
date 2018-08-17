def get_charities(db):
	doc_ref = db.collection(u'charityOfTheWeek').document(u'charityVotes').get().to_dict()
	return doc_ref

def increment(db, charityUpdate):
	data = charityUpdate
	print(">>" + str(data))
	#db.collection(u'users').document(u'{:}'.format(user)).document(u'suggestion').set(data)
	user_ref = db.collection(u'charityOfTheWeek').document(u'charityVotes')
	user_ref.update(data)

# finds top suggestion and pushes to database
def increment_charity(db, charityName):
	charities = get_charities(db)
	updatedCharity = charities[charityName] + 1
	charities[charityName] = updatedCharity
	increment(db, charities)