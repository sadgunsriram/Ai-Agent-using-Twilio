from app.db.session import SessionLocal
from app.db.crud import get_next_student_to_call, create_call_log
from app.services.twilio_service import call_student

# Track students called in current campaign
called_students = set()


def start_next_call(start_new=False):

    global called_students

    if start_new:
        called_students = set()
        print("🚀 Starting calling campaign...")

    db = SessionLocal()

    try:
        student = get_next_student_to_call(db, called_students)

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

        called_students.add(student.id)

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