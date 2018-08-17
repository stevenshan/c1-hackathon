import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from find_charity import *

user = 'johnpaul'

def connect_to_db():
	cred = credentials.Certificate('firestoresample-9aa84-firebase-adminsdk-pdwy2-e32cd07ccf.json')
	firebase_admin.initialize_app(cred, {
  		'projectId': 'firestoresample-9aa84',
	})
	db = firestore.client()
	return db

def get_interests(db):
	doc_ref = db.collection(u'users').document(u'{:}'.format(user)).get().to_dict()
	return doc_ref['interests']

def write_current_suggestion(db, suggestion):
	data = {u'suggestion': 
				{u'name': suggestion['charityName'],
				u'mission': suggestion['mission']}
			}
	#db.collection(u'users').document(u'{:}'.format(user)).document(u'suggestion').set(data)
	user_ref = db.collection(u'users').document(u'{:}'.format(user))
	user_ref.update(data)


def access_suggestions(db):
	#db = connect_to_db()
	interests = get_interests(db)
	suggestions = [s['ein'] for s in get_suggestions(interests) if not(s['mission'] == 'null')]
	return suggestions

# finds top suggestion and pushes to database
def update_suggestion():
	db = connect_to_db()
	interests = get_interests(db)
	suggestions = [s for s in get_suggestions(interests) if not(s['mission'] == 'null')]
	suggestion = suggestions[0]
	write_current_suggestion(db, suggestion)

#update_suggestion()
