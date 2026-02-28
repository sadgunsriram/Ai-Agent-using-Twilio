from dotenv import load_dotenv
import os

load_dotenv()

# -------------------------------
#  Database
# -------------------------------
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/ai_calling_agent"

# -------------------------------
#  Twilio Credentials
# -------------------------------
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
BASE_URL = os.getenv("BASE_URL")

# -------------------------------
#  Multi Telecaller Support
# -------------------------------
telecaller_env = os.getenv("TELECALLER_NUMBERS", "")

TELECALLER_NUMBERS = [
    number.strip()
    for number in telecaller_env.split(",")
    if number.strip()
]

if not TELECALLER_NUMBERS:
    raise ValueError("❌ TELECALLER_NUMBERS not configured in .env")