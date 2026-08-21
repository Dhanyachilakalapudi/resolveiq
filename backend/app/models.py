from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime

from .database import Base


class ExceptionRecord(Base):
    __tablename__ = "exceptions"

    id = Column(Integer, primary_key=True, index=True)
    exception_id = Column(String, unique=True, index=True, nullable=False)
    invoice_id = Column(String, nullable=False)
    vendor = Column(String, nullable=False)

    exception_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    expected_value = Column(Float, nullable=True)
    actual_value = Column(Float, nullable=True)
    difference = Column(Float, nullable=True)

    severity = Column(String, nullable=False, default="MEDIUM")
    status = Column(String, nullable=False, default="PENDING")

    confidence = Column(Float, nullable=True)
    recommended_action = Column(String, nullable=True)
    ai_reason = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
