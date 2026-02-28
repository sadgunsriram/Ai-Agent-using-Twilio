from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import text
from app.db.models import Student, CallLog


def get_next_student_to_call(db: Session):
    subquery = db.query(CallLog.student_id)

    return (
        db.query(Student)
        .filter(~Student.id.in_(subquery))
        .order_by(Student.id.asc())
        .first()
    )


def create_call_log(db: Session, student_id: int, call_sid: str):
    log = CallLog(
        student_id=student_id,
        call_sid=call_sid,
        call_status="initiated"
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_call_log_by_sid(db: Session, call_sid: str):
    return db.query(CallLog).filter(CallLog.call_sid == call_sid).first()


def complete_call(db: Session, call_sid: str, response: str):
    log = db.query(CallLog).filter(CallLog.call_sid == call_sid).first()
    if log:
        log.response_type = response
        log.call_status = "completed"
        log.completed_at = func.now()
        db.commit()
        return log


# 🔁 RESET SYSTEM TO START CALLING FROM BEGINNING
def reset_all_calls(db: Session):
    print("🔁 Resetting all call logs and responses...")

    db.execute(text("DELETE FROM call_logs"))
    db.commit()
