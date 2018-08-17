import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def connect_to_db():
	cred = credentials.Certificate('firestoresample-9aa84-firebase-adminsdk-pdwy2-e32cd07ccf.json')
	firebase_admin.initialize_app(cred, {
  		'projectId': 'firestoresample-9aa84',
	})
	db = firestore.client()
	return db

def get_charities(db):
	doc_ref = db.collection(u'charityOfTheWeek').document(u'charityVotes').get().to_dict()
	return doc_ref

def increment(db, charityUpdate):
	data = charityUpdate
	#db.collection(u'users').document(u'{:}'.format(user)).document(u'suggestion').set(data)
	user_ref = db.collection(u'charityOfTheWeek').document(u'charityVotes')
	user_ref.update(data)


# finds top suggestion and pushes to database
def increment_charity(charityName):
	db = connect_to_db()
	charities = get_charities(db)
	updatedCharity = charities[charityName] + 1
	charities[charityName] = updatedCharity
	increment(db, charities)