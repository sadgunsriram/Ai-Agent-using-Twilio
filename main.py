from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import SessionLocal
from app.db.crud import reset_all_calls  
from app.api.twilio_webhooks import router as twilio_router
from app.services.call_orchestrator import start_next_call

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(twilio_router)


@app.post("/start-calling")
def start_calling():
    db = SessionLocal()

    try:
        # 🔁 Reset when button is pressed
        reset_all_calls(db)
        print("🔁 Call logs reset. Starting fresh batch...")

    finally:
        db.close()

    # 🚀 Start first call
    return start_next_call()


@app.post("/reset-calls")
def reset_calls():
    db = SessionLocal()
    try:
        reset_all_calls(db)
        return {"status": "CALLS_RESET_SUCCESSFULLY"}
    finally:
        db.close()


@app.get("/")
def health():
    return {"status": "ok"}




# http://192.168.36.183:8000/start-calling
# For run the code 
# uvicorn main:app --reload                                 - this only runs with localhost 

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload      - this runs with ip 
