from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

app = FastAPI()

# --- SETUP FIREBASE ---
# Check if we are already initialized to avoid errors on re-loads
if not firebase_admin._apps:
    # 1. Try to load from Vercel Environment Variable (Best for Deployment)
    env_creds = os.environ.get("FIREBASE_CREDENTIALS")
    
    if env_creds:
        cred_dict = json.loads(env_creds)
        cred = credentials.Certificate(cred_dict)
    # 2. If no Env Var, try to load local file (Best for Local Testing)
    elif os.path.exists("service_account.json"):
        cred = credentials.Certificate("service_account.json")
    else:
        # If neither exists, the server cannot start properly
        print("Error: No Firebase credentials found!")
        cred = None

    if cred:
        firebase_admin.initialize_app(cred)

# --- DATA MODEL ---
class FireAlert(BaseModel):
    location: str
    confidence: float

# --- THE ENDPOINT ---
@app.post("/notify")
def send_notification(alert: FireAlert):
    if not firebase_admin._apps:
        raise HTTPException(status_code=500, detail="Firebase not initialized")

    try:
        # Create the message for the Flutter app
        message = messaging.Message(
            notification=messaging.Notification(
                title="🔥 FIRE DETECTED!",
                body=f"Location: {alert.location} (Conf: {alert.confidence})",
            ),
            topic="fire_alerts", # This MUST match your Flutter code
        )
        # Send it
        response = messaging.send(message)
        return {"status": "success", "message_id": response}
    except Exception as e:
        return {"status": "error", "details": str(e)}