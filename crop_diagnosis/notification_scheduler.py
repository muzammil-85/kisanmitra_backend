import firebase_admin
from firebase_admin import messaging, firestore
from datetime import datetime, timezone

# Initialize Firebase only once
if not firebase_admin._apps:
    firebase_admin.initialize_app()

def send_notifications(request):
    db = firestore.client()
    now = datetime.now(timezone.utc).isoformat()

    # Get notifications that are due and not yet sent
    docs = db.collection("scheduled_notifications")\
             .where("sent", "==", False)\
             .where("send_at", "<=", now).stream()

    sent_count = 0

    for doc in docs:
        data = doc.to_dict()

        message = messaging.Message(
            notification=messaging.Notification(
                title=data["title"],
                body=data["body"]
            ),
            token=data["token"]
        )

        try:
            messaging.send(message)
            # Mark as sent
            db.collection("scheduled_notifications").document(doc.id).update({"sent": True})
            sent_count += 1
        except Exception as e:
            print(f"Failed to send notification: {e}")

    return f"Sent {sent_count} notifications", 200
