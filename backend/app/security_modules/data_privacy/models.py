from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from database import Base


class DataPrivacyAssessment(Base):
    __tablename__ = "data_privacy_assessments"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, index=True)
    assessment_date = Column(DateTime(timezone=True), server_default=func.now())
    pii_detected = Column(Integer, default=0)
    pii_masked = Column(Integer, default=0)
    privacy_score = Column(Float, default=0.0)
    findings = Column(JSON)


class PIIRecord(Base):
    __tablename__ = "pii_records"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, index=True)
    pii_type = Column(String(100))
    location = Column(String(500))
    masked = Column(Boolean, default=False)
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
