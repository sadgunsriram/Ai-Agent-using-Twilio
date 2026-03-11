from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, nullable=False)
    student_name = Column(String(100), nullable=False)
    student_phone = Column(String(15), unique=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    last_call_time = Column(DateTime)
    last_response = Column(String(20))


class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    call_sid = Column(String(100), unique=True, nullable=False)
    call_status = Column(String(20), default="initiated")
    response_type = Column(String(20))

    retry_count = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)


class YesResponse(Base):
    __tablename__ = "yes_responses"

    id = Column(Integer, primary_key=True)
    call_log_id = Column(Integer, ForeignKey("call_logs.id"))
    created_at = Column(DateTime, server_default=func.now())


# Twilio configuration
class TwilioConfig(Base):
    __tablename__ = "twilio_config"

    id = Column(Integer, primary_key=True, index=True)

    account_sid = Column(String(100), nullable=False)
    auth_token = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)

    status = Column(String(20), default="active")

    created_at = Column(DateTime, server_default=func.now())


# Telecaller numbers
class Telecaller(Base):
    __tablename__ = "telecallers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False)

    status = Column(String(20), default="active")

    created_at = Column(DateTime, server_default=func.now())