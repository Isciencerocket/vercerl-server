from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("service-account.json")
firebase_admin.initialize_app(cred)

@app.route('/api/notify', methods=['POST'])
def send_notification():
    data = request.json
    message = messaging.Message(
        notification=messaging.Notification(
            title="🔥 FIRE DETECTED!",
            body=f"Location: {data.get('location', 'Unknown')}",
        ),
        topic="fire_alerts", # All apps subscribed to this topic will get it
    )
    response = messaging.send(message)
    return jsonify({"status": "sent", "id": response})