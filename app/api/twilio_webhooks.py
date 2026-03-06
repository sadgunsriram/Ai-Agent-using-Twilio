from fastapi import APIRouter, Request
from fastapi.responses import Response
from app.db.session import SessionLocal
from app.db.crud import complete_call, get_call_log_by_sid
from app.services.response_handler import handle_yes_response, handle_no_response
from app.services.call_orchestrator import start_next_call
from app.config import TELECALLER_NUMBERS

router = APIRouter()


# --------------------------------------------------
# 🔁 Generate Dial TwiML (Retry Logic)
# --------------------------------------------------
def generate_dial_twiml(index: int = 0):

    if index >= len(TELECALLER_NUMBERS):
        return """
        <Response>
            <Say>All our counselors are currently busy. We will call you back shortly.</Say>
            <Hangup/>
        </Response>
        """

    number = TELECALLER_NUMBERS[index]

    return f"""
    <Response>
        <Say>Connecting you to our counselor now.</Say>
        <Dial action="/twilio/dial-status?index={index}" timeout="15">
            <Number>{number}</Number>
        </Dial>
    </Response>
    """


# --------------------------------------------------
# 🎤 Student ANSWERED → Treat as YES
# --------------------------------------------------
@router.post("/twilio/voice")
async def voice_response(request: Request):

    form = await request.form()
    call_sid = form.get("CallSid")

    if not call_sid:
        return Response("<Response><Hangup/></Response>", media_type="application/xml")

    db = SessionLocal()

    try:
        log = get_call_log_by_sid(db, call_sid)

        if log and log.call_status != "completed":
            complete_call(db, call_sid, "YES")
            handle_yes_response(log)

    finally:
        db.close()

    twiml = generate_dial_twiml(0)
    return Response(content=twiml.strip(), media_type="application/xml")


# --------------------------------------------------
# 🔁 TELECALLER RETRY HANDLER
# --------------------------------------------------
@router.post("/twilio/dial-status")
async def dial_status_callback(request: Request):

    form = await request.form()

    dial_status = form.get("DialCallStatus")
    index = int(request.query_params.get("index", 0))

    # If telecaller answered and call completed
    if dial_status == "completed":
        return Response("<Response></Response>", media_type="application/xml")

    # If telecaller failed → try next
    if dial_status in ["busy", "no-answer", "failed", "canceled"]:
        next_index = index + 1
        twiml = generate_dial_twiml(next_index)
        return Response(content=twiml.strip(), media_type="application/xml")

    return Response("<Response></Response>", media_type="application/xml")


# --------------------------------------------------
# 📡 STUDENT CALL STATUS HANDLER
# --------------------------------------------------
@router.post("/twilio/status")
async def status_callback(request: Request):

    form = await request.form()

    call_sid = form.get("CallSid")
    call_status = form.get("CallStatus")

    db = SessionLocal()

    try:
        log = get_call_log_by_sid(db, call_sid)

        if not log:
            return ""

        if call_status in ["busy", "failed", "no-answer", "canceled"]:
            if log.call_status != "completed":
                complete_call(db, call_sid, "NO")
                handle_no_response(log)

        if call_status == "completed":
            result = start_next_call(start_new=False)

            if result.get("status") == "ALL_CALLS_COMPLETED":
                print("🎯 All students processed.")

    finally:
        db.close()

    return ""

