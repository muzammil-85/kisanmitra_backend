import os
import firebase_admin
from firebase_admin import credentials, firestore

path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)
db = firestore.client()
