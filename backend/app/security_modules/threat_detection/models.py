from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.sql import func
from database import Base


class SecurityAlert(Base):
    __tablename__ = "security_alerts"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, index=True)
    threat_type = Column(String(100))
    severity = Column(String(50))
    description = Column(String(2000))
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="OPEN")
    details = Column(JSON)


class ThreatIndicator(Base):
    __tablename__ = "threat_indicators"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, index=True)
    indicator_type = Column(String(100))
    confidence_score = Column(Float, default=0.0)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(JSON)
