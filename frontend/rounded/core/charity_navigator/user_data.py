# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
from .find_charity import *
from .. import firebase 
from .. import redis
from flask import current_app as app

def write_current_suggestion(suggestion):
	data = {
		'suggestion': {
			'name': suggestion['charityName'],
			'mission': suggestion['mission']
		}
	}

	# user_ref = db.collection(u'users').document(u'{:}'.format(user))
	# user_ref.update(data)

	user = app.config.get("USER")
	if user == None:
		return
	redis.hset("user:" + str(user), "data", data)	

def access_suggestions():
	#db = connect_to_db()
	interests = firebase.get_interests()
	suggestions = [s['ein'] for s in get_suggestions(interests) if not(s['mission'] == '')]
	return suggestions

# finds top suggestion and pushes to database
def update_suggestion():
	# db = firebase.getDB() #connect_to_db()
	interests = firebase.get_interests()
	suggestions = [s for s in get_suggestions(interests) if not(s['mission'] == '')]
	suggestion = suggestions[0]
	write_current_suggestion(suggestion)

#update_suggestion()
