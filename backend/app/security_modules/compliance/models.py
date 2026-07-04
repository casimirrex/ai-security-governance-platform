from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Float
from sqlalchemy.sql import func
from app.database import Base


class ComplianceFramework(Base):
    __tablename__ = "compliance_frameworks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(String(1000))
    framework_type = Column(String(100))
    version = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"

    id = Column(Integer, primary_key=True, index=True)
    framework_id = Column(Integer, index=True)
    model_id = Column(Integer, index=True)
    check_name = Column(String(255))
    description = Column(String(1000))
    control_id = Column(String(100))
    status = Column(String(50))
    compliance_score = Column(Float, default=0.0)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())
    findings = Column(JSON)
    remediation = Column(String(2000))


class ComplianceAuditLog(Base):
    __tablename__ = "compliance_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    check_id = Column(Integer, index=True)
    action = Column(String(255))
    user = Column(String(255))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(JSON)
