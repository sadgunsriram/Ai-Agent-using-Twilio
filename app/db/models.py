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


class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    call_sid = Column(String(100), unique=True, nullable=False)
    call_status = Column(String(20), default="initiated")   # initiated / completed
    response_type = Column(String(20))                      # YES / NO / BUSY

    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)


class YesResponse(Base):
    __tablename__ = "yes_responses"

    id = Column(Integer, primary_key=True)
    call_log_id = Column(Integer, ForeignKey("call_logs.id"))
    created_at = Column(DateTime, server_default=func.now())
