from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.security_modules.threat_detection.service import ThreatDetectionService
from app.security_modules.threat_detection.models import SecurityAlert

router = APIRouter()


class ThreatAlertInput(BaseModel):
    model_id: int
    threat_type: str
    severity: str
    description: str


class ThreatAlertResponse(BaseModel):
    id: int
    timestamp: str
    status: str
    model_id: int
    threat_type: str
    severity: str


class ThreatMetrics(BaseModel):
    model_id: int
    prediction_confidence_variance: float = 0
    unexpected_access_patterns: bool = False
    data_distribution_shift: float = 0
    failed_auth_attempts: int = 0


@router.post("/alert", response_model=ThreatAlertResponse)
def create_threat_alert(alert: ThreatAlertInput, db: Session = Depends(get_db)):
    """Log a security threat or anomaly."""
    security_alert = SecurityAlert(
        model_id=alert.model_id,
        threat_type=alert.threat_type,
        severity=alert.severity,
        description=alert.description,
        status="OPEN",
        details={"created_via_api": True},
    )
    db.add(security_alert)
    db.commit()
    db.refresh(security_alert)

    return ThreatAlertResponse(
        id=security_alert.id,
        timestamp=security_alert.detected_at.isoformat(),
        status=security_alert.status,
        model_id=security_alert.model_id,
        threat_type=security_alert.threat_type,
        severity=security_alert.severity,
    )


@router.post("/detect")
def detect_threats(metrics: ThreatMetrics, db: Session = Depends(get_db)):
    """Detect threats based on model metrics."""
    service = ThreatDetectionService()
    alerts = service.detect_threats(db, metrics.model_id, metrics.dict())
    return {
        "model_id": metrics.model_id,
        "alert_count": len(alerts),
        "alerts": alerts,
    }


@router.get("/alerts/{model_id}")
def get_model_alerts(model_id: int, db: Session = Depends(get_db)):
    """Get security alerts for a model."""
    alerts = db.query(SecurityAlert).filter(
        SecurityAlert.model_id == model_id
    ).order_by(SecurityAlert.detected_at.desc()).limit(10).all()

    return {
        "model_id": model_id,
        "alert_count": len(alerts),
        "alerts": [
            {
                "alert_id": a.id,
                "threat_type": a.threat_type,
                "severity": a.severity,
                "timestamp": a.detected_at.isoformat(),
                "status": a.status,
            }
            for a in alerts
        ]
    }


@router.get("/dashboard")
def get_threat_dashboard(db: Session = Depends(get_db)):
    """Get overall threat detection dashboard."""
    all_alerts = db.query(SecurityAlert).all()

    severity_counts = {
        "critical": sum(1 for a in all_alerts if a.severity == "CRITICAL"),
        "high": sum(1 for a in all_alerts if a.severity == "HIGH"),
        "medium": sum(1 for a in all_alerts if a.severity == "MEDIUM"),
        "low": sum(1 for a in all_alerts if a.severity == "LOW"),
        "info": sum(1 for a in all_alerts if a.severity == "INFO"),
    }

    return {
        "total_alerts": len(all_alerts),
        "critical_alerts": severity_counts["critical"],
        "high_alerts": severity_counts["high"],
        "medium_alerts": severity_counts["medium"],
        "low_alerts": severity_counts["low"],
        "info_alerts": severity_counts["info"],
        "trends": {
            "alerts_24h": len([a for a in all_alerts if a.detected_at]),
            "open_alerts": sum(1 for a in all_alerts if a.status == "OPEN"),
        }
    }
