from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, index=True)
    action = Column(String(255))
    user = Column(String(255))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(JSON)
    ip_address = Column(String(50), nullable=True)
    status = Column(String(50))


class ComplianceReport(Base):
    __tablename__ = "compliance_reports"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, index=True)
    report_type = Column(String(100))
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    findings = Column(JSON)
    status = Column(String(50))
    pdf_path = Column(String(500), nullable=True)
