from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.twilio_webhooks import router as twilio_router
from app.services.call_orchestrator import start_next_call


app = FastAPI()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Twilio webhook routes
app.include_router(twilio_router)


# 🚀 Start calling campaign
@app.post("/start-calling")
def start_calling():
    return start_next_call(start_new=True)


# Health check
@app.get("/")
def health():
    return {"status": "ok"}


# For run the code
# uvicorn main:app --reload                                 - localhost
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload      - accessible via IP