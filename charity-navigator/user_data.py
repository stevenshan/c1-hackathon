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

def get_interests(db):
	doc_ref = db.collection(u'users').document(u'johnpaul').get().to_dict()
	return doc_ref['interests']

def write_current_suggestion(suggestion):
	data = {u'name': ,
			u'url': }

