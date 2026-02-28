from twilio.rest import Client
from app.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    BASE_URL
)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def call_student(phone_number: str):
    call = client.calls.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        url=f"{BASE_URL}/twilio/voice",
        status_callback=f"{BASE_URL}/twilio/status",
        status_callback_event=[
    "initiated",
    "ringing",
    "answered",
    "completed"
],

        status_callback_method="POST"
    )
    return call.sid


