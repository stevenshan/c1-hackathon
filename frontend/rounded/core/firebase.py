import os
import json
from flask import current_app as app
from rounded.core import redis

# from firebase_admin import credentials
# from firebase_admin import firestore 
# import firebase_admin

# def getDB():
#     try:
#         db_client = firestore.client()
#     except Exception as e:
#         raise ValueError("Error connecting to Firebase: " + str(e))

#     return db_client

# def connect():
#     try:
#         temp = getDB()
#         if temp == None:
#             raise ValueError("")
#         return
#     except:
#         pass

#     CERT_FILE = 'firebase_key.json'
#     path = os.path.join(
#         os.getcwd(),
#         os.path.dirname(__file__),
#         CERT_FILE
#     )

#     cred = credentials.Certificate(path)
#     firebase_admin.initialize_app(
#         cred, 
#         {
#             'projectId': 'firestoresample-9aa84',
#         },
#     )

def get_interests():
    # user_ref = db.collection(u'users').document(u'johnpaul')
    # return user_ref.get().to_dict().get("interests", [])

    user = app.config.get("USER")
    if user == None:
        return []
    else:
        raw = redis.get("interests:" + str(user))

        if raw == None:
            return []
        return json.loads(raw)

def change_interests(listOfInterests):
    # user_ref = db.collection(u'users').document(u'johnpaul')
    # data = {u'interests':listOfInterests}
    # user_ref.update(data)

    user = app.config.get("USER")
    if user == None:
        return
    else:
        raw = json.dumps(listOfInterests)
        redis.set("interests:" + str(user), raw)
