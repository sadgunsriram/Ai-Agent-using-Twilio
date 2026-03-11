from twilio.rest import Client
from app.db.session import SessionLocal
from app.db.crud import get_twilio_config
from app.config import BASE_URL


def call_student(phone):

    db = SessionLocal()

    try:
        config = get_twilio_config(db)

        if not config:
            raise Exception("Twilio configuration not found")

        client = Client(
            config.account_sid,
            config.auth_token
        )

        call = client.calls.create(
            to=phone,
            from_=config.phone_number,
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

        return call.sid

    finally:
        db.close()