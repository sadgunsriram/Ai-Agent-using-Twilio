from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# -------------------------------
# Database Configuration
# -------------------------------
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/ai_calling_agent"

# -------------------------------
# Base URL for Twilio Webhooks
# -------------------------------
BASE_URL = os.getenv("BASE_URL")