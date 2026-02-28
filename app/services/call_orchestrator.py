from app.db.session import SessionLocal
from app.db.crud import get_next_student_to_call, create_call_log
from app.services.twilio_service import call_student


def start_next_call():
    db = SessionLocal()

    try:
        student = get_next_student_to_call(db)

        if not student:
            print("✅ All students processed. Stopping.")
            return {"status": "ALL_CALLS_COMPLETED"}

        print(f"📲 Calling Student: {student.student_name}")

        call_sid = call_student(student.student_phone)

        create_call_log(
            db=db,
            student_id=student.id,
            call_sid=call_sid
        )

        return {
            "status": "CALL_STARTED",
            "student_id": student.id,
            "call_sid": call_sid
        }

    except Exception as e:
        print("❌ Error in start_next_call:", e)
        return {"status": "ERROR", "message": str(e)}

    finally:
        db.close()