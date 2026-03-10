from fastapi import APIRouter, Request
from fastapi.responses import Response
from app.db.session import SessionLocal
from app.db.crud import complete_call, get_call_log_by_sid, get_active_telecallers
from app.services.response_handler import handle_yes_response, handle_no_response
from app.services.call_orchestrator import start_next_call
from app.config import BASE_URL

router = APIRouter()



#  Generate Dial TwiML (Retry Logic)

def generate_dial_twiml(index: int = 0):

    db = SessionLocal()

    try:
        telecallers = get_active_telecallers(db)
        numbers = [t.phone_number for t in telecallers]

    finally:
        db.close()

    print("📞 Telecaller list:", numbers)

    if not numbers:
        return """
<Response>
    <Say>No counselors available right now.</Say>
    <Hangup/>
</Response>
"""

    if index >= len(numbers):
        return """
<Response>
    <Say>All our counselors are currently busy. We will call you back shortly.</Say>
    <Hangup/>
</Response>
"""

    number = numbers[index]

    return f"""
<Response>
    <Say>Please wait while we connect you to our counselor.</Say>
    <Dial
        action="{BASE_URL}/twilio/dial-status?index={index}"
        method="POST"
        timeout="20"
        answerOnBridge="true">
        <Number>{number}</Number>
    </Dial>
</Response>
"""



# 🎤 Student ANSWERED → Treat as YES

@router.post("/twilio/voice")
async def voice_response(request: Request):

    form = await request.form()
    call_sid = form.get("CallSid")

    print("📞 Student answered:", call_sid)

    if not call_sid:
        return Response("<Response><Hangup/></Response>", media_type="application/xml")

    db = SessionLocal()

    try:
        log = get_call_log_by_sid(db, call_sid)

        if log and log.call_status != "completed":
            print("✅ Saving YES response")

            complete_call(db, call_sid, "YES")
            handle_yes_response(log)

        # Fetch telecallers from DB
        telecallers = get_active_telecallers(db)
        numbers = [t.phone_number for t in telecallers]

    finally:
        db.close()

    if not numbers:
        return Response(
            "<Response><Say>No counselors available.</Say></Response>",
            media_type="application/xml"
        )

    telecaller = numbers[0]

    twiml = f"""
<Response>
    <Say>Please wait while we connect you to our counselor.</Say>
    <Dial
        action="{BASE_URL}/twilio/dial-status?index=0"
        method="POST"
        timeout="20"
        answerOnBridge="true">
        <Number>{telecaller}</Number>
    </Dial>
</Response>
"""

    print("📜 TwiML sent to Twilio:\n", twiml)

    return Response(content=twiml.strip(), media_type="application/xml")



# 🔁 TELECALLER RETRY HANDLER

@router.post("/twilio/dial-status")
async def dial_status_callback(request: Request):

    form = await request.form()

    dial_status = form.get("DialCallStatus")
    index = int(request.query_params.get("index", 0))

    print("📡 Telecaller dial status:", dial_status)
    print("📡 Telecaller index:", index)

    if dial_status == "completed":
        print("✅ Telecaller connected successfully")
        return Response("<Response></Response>", media_type="application/xml")

    if dial_status in ["busy", "no-answer", "failed", "canceled"]:
        next_index = index + 1
        print("⚠️ Telecaller unavailable. Trying next telecaller:", next_index)

        twiml = generate_dial_twiml(next_index)

        return Response(content=twiml.strip(), media_type="application/xml")

    return Response("<Response></Response>", media_type="application/xml")



# 📡 STUDENT CALL STATUS HANDLER

@router.post("/twilio/status")
async def status_callback(request: Request):

    form = await request.form()

    call_sid = form.get("CallSid")
    call_status = form.get("CallStatus")

    print("📡 Call SID:", call_sid)
    print("📡 Call status:", call_status)

    if not call_sid:
        return ""

    db = SessionLocal()

    try:
        log = get_call_log_by_sid(db, call_sid)

        if not log:
            print("⚠️ No call log found")
            return ""

        
        # ❌ STUDENT DID NOT ANSWER
        
        if call_status in ["busy", "failed", "no-answer", "canceled"]:

            if log.call_status != "completed":

                print("❌ Student did not answer → Saving NO")

                complete_call(db, call_sid, "NO")
                handle_no_response(log)

                print("📞 Calling next student...")
                start_next_call(start_new=False)

        
        # 📞 CALL COMPLETED
        
        elif call_status == "completed":

            print("📞 Call completed")

            if log.call_status != "completed":
                complete_call(db, call_sid, "NO")

            print("📞 Calling next student...")
            start_next_call(start_new=False)

    finally:
        db.close()

    return ""