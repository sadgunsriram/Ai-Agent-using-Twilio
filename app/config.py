from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# -------------------------------
# Database
# -------------------------------
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/ai_calling_agent"

# -------------------------------
# Twilio Credentials
# -------------------------------
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Base URL for Twilio Webhooks
BASE_URL = os.getenv("BASE_URL")