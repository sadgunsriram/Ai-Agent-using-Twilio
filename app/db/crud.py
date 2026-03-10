from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.models import Student, CallLog, Telecaller, TwilioNumber


def get_next_student_to_call(db: Session, called_students):

    student = (
        db.query(Student)
        .filter(~Student.id.in_(called_students))
        .order_by(Student.id.asc())
        .first()
    )

    return student


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

    if not log:
        return None

    log.response_type = response
    log.call_status = "completed"
    log.completed_at = func.now()

    student = db.query(Student).filter(Student.id == log.student_id).first()

    if student:
        student.last_call_time = func.now()
        student.last_response = response

    db.commit()
    db.refresh(log)

    return log


# --------------------------------------------------
# TELECALLERS
# --------------------------------------------------

def get_active_telecallers(db: Session):

    return (
        db.query(Telecaller)
        .filter(Telecaller.status == "active")
        .all()
    )


# --------------------------------------------------
# TWILIO NUMBER
# --------------------------------------------------

def get_twilio_number(db: Session):

    return (
        db.query(TwilioNumber)
        .filter(TwilioNumber.status == "active")
        .first()
    )