
from google.cloud import firestore

db = firestore.Client()

class Vegetable:
    def __init__(self, doc_id, name, image_url):
        self.id = doc_id
        self.name = name
        self.image_url = image_url

    def __str__(self):
        return self.name

    @classmethod
    def all(cls):
        """
        Fetch all vegetables from Firestore
        """
        docs = db.collection('crops').document('vegetable').collection('items').stream()
        vegetables = []
        for doc in docs:
            data = doc.to_dict()
            vegetables.append(
                cls(doc.id, data.get('name', ''), data.get('image', ''))
            )
        return vegetables

    @classmethod
    def get(cls, doc_id):
        """
        Get a single vegetable document by ID
        """
        doc = db.collection('crops').document('vegetable').collection('items').document(doc_id).get()
        if doc.exists:
            data = doc.to_dict()
            return cls(doc_id, data.get('name'), data.get('image'))
        return None

    def save(self):
        """
        Save or update the vegetable document in Firestore
        """
        doc_ref = db.collection('crops').document('vegetable').collection('items').document(self.id)
        doc_ref.set({
            'name': self.name,
            'image': self.image_url
        })

    def delete(self):
        """
        Delete the vegetable document from Firestore
        """
        db.collection('crops').document('vegetable').collection('items').document(self.id).delete()