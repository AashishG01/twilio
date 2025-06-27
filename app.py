from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse


# Load .env variables
load_dotenv()

app = FastAPI()

# Twilio client setup
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

client = Client(TWILIO_SID, TWILIO_AUTH)

# Request body model
class MessageRequest(BaseModel):
    to: str
    message: str

@app.post("/send-message")
def send_message(req: MessageRequest):
    try:
        to_number = f"whatsapp:{req.to}"
        sent = client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=to_number,
            body=req.message
        )
        return {"success": True, "sid": sent.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/whatsapp-webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
):
    print(f"📩 Message from {From}: {Body}")

    # You can now store this in a DB, trigger responses, etc.
    return "Received"