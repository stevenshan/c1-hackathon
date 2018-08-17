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

