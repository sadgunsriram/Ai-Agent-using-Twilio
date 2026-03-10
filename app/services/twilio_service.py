from twilio.rest import Client
from dotenv import load_dotenv
from pathlib import Path
import os

from app.db.session import SessionLocal
from app.db.crud import get_twilio_number

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
BASE_URL = os.getenv("BASE_URL")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def call_student(phone):

    db = SessionLocal()

    try:
        twilio = get_twilio_number(db)

        if not twilio:
            raise Exception("No Twilio number configured in DB")

        twilio_number = twilio.phone_number

    finally:
        db.close()

    print("📞 Calling student:", phone)
    print("📞 From number:", twilio_number)

    call = client.calls.create(
        to=phone,
        from_=twilio_number,
        url=f"{BASE_URL}/twilio/voice",
        status_callback=f"{BASE_URL}/twilio/status",
        status_callback_method="POST",
        status_callback_event=[
            "initiated",
            "ringing",
            "answered",
            "completed"
        ]
    )

    print("📞 Call SID:", call.sid)

    return call.sid