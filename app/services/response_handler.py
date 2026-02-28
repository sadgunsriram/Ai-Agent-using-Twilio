
import requests
import logging

logging.basicConfig(level=logging.INFO)


# --------------------------------------------------
# ✅ HANDLE YES RESPONSE
# --------------------------------------------------
def handle_yes_response(call_log):
    print("✅ Student Available")

    payload = {
        "student_id": call_log.student_id,
        "call_sid": call_log.call_sid,
        "response": "YES"
    }


# --------------------------------------------------
# ❌ HANDLE NO RESPONSE
# --------------------------------------------------
def handle_no_response(call_log):
    print("❌ Student Unavailable")

    payload = {
        "student_id": call_log.student_id,
        "call_sid": call_log.call_sid,
        "response": "NO"
    }
