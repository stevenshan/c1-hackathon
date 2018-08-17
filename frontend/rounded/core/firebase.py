import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 
import os

def connect():
    CERT_FILE = 'firebase_key.json'
    path = os.path.join(
        os.getcwd(),
        os.path.dirname(__file__),
        CERT_FILE
    )

    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(
        cred, 
        {
            'projectId': 'firestoresample-9aa84',
        },
    )

def getDB():
    try:
        db_client = firestore.client()
    except Exception as e:
        return "Error connecting to Firebase: " + str(e)

    return db_client

def get_interests(db):
    user_ref = db.collection(u'users').document(u'johnpaul')
    return user_ref.get().to_dict().get("interests", [])

def change_interests(db, listOfInterests):
    user_ref = db.collection(u'users').document(u'johnpaul')
    data = {u'interests':listOfInterests}
    user_ref.update(data)