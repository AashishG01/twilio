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
TWILIO_ACCOUNT_SID="ACc91e651740f9320c4fb012a4bf29fea8"
TWILIO_AUTH_TOKEN="d63b9a1ea103419783ab13b0355b1170"
TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"

# Twilio client setup
TWILIO_SID = TWILIO_ACCOUNT_SID
TWILIO_AUTH = TWILIO_AUTH_TOKEN
TWILIO_WHATSAPP_FROM = TWILIO_WHATSAPP_FROM


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


# @app.post("/whatsapp-webhook", response_class=PlainTextResponse)
# async def whatsapp_webhook(
#     From: str = Form(...),
#     Body: str = Form(...),
# ):
#     print(f"📩 Message from {From}: {Body}")

#     # You can now store this in a DB, trigger responses, etc.
#     return "Received"