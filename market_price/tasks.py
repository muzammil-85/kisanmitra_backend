
import requests
from datetime import datetime
from firebase_admin import firestore

def fetch_and_store_mandi_prices():
    print("Fetching mandi price data...")

    url = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json'
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch data from API")
        return

    data = response.json()
    records = data.get("records", [])
    db = firestore.client()

    for record in records:
        doc_ref = db.collection("mandi_prices").document()
        doc_ref.set({
            "state": record.get("state", ""),
            "district": record.get("district", ""),
            "market": record.get("market", ""),
            "commodity": record.get("commodity", ""),
            "variety": record.get("variety", ""),
            "grade": record.get("grade", ""),
            "arrival_date": record.get("arrival_date", ""),
            "min_price": record.get("min_price", ""),
            "max_price": record.get("max_price", ""),
            "modal_price": record.get("modal_price", ""),
            "timestamp": datetime.utcnow()
        })

    print(f"{len(records)} records stored in Firestore.")