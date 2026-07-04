from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from database import Base


class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(String(1000))
    model_type = Column(String(100))
    framework = Column(String(100))
    version = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SecurityRiskAssessment(Base):
    __tablename__ = "security_risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, index=True)
    assessment_date = Column(DateTime(timezone=True), server_default=func.now())

    adversarial_robustness_score = Column(Float, default=0.0)
    data_poisoning_risk = Column(Float, default=0.0)
    model_stealing_risk = Column(Float, default=0.0)
    membership_inference_risk = Column(Float, default=0.0)
    privacy_leakage_risk = Column(Float, default=0.0)

    overall_risk_score = Column(Float, default=0.0)
    risk_level = Column(String(50))

    findings = Column(JSON)
    recommendations = Column(JSON)
    status = Column(String(50), default="completed")


class VulnerabilityFinding(Base):
    __tablename__ = "vulnerability_findings"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, index=True)
    vulnerability_type = Column(String(100))
    severity = Column(String(50))
    description = Column(String(2000))
    cve_id = Column(String(100), nullable=True)
    remediation = Column(String(2000))
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved = Column(Boolean, default=False)
