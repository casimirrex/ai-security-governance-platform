from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class ThreatAlert(BaseModel):
    model_id: int
    threat_type: str
    severity: str
    description: str


@router.post("/alert")
def create_threat_alert(alert: ThreatAlert, db: Session = Depends(get_db)):
    """Log a security threat or anomaly."""
    return {
        "alert_id": 1,
        "timestamp": datetime.now().isoformat(),
        "status": "OPEN",
        "model_id": alert.model_id,
        "threat_type": alert.threat_type,
        "severity": alert.severity,
    }


@router.get("/alerts/{model_id}")
def get_model_alerts(model_id: int, db: Session = Depends(get_db)):
    """Get security alerts for a model."""
    return {
        "model_id": model_id,
        "alert_count": 2,
        "alerts": [
            {
                "alert_id": 1,
                "threat_type": "UNUSUAL_PREDICTION_PATTERN",
                "severity": "MEDIUM",
                "timestamp": "2024-01-15T10:30:00Z",
                "status": "OPEN",
            },
            {
                "alert_id": 2,
                "threat_type": "HIGH_CONFIDENCE_ANOMALY",
                "severity": "LOW",
                "timestamp": "2024-01-15T09:15:00Z",
                "status": "RESOLVED",
            },
        ]
    }


@router.get("/dashboard")
def get_threat_dashboard():
    """Get overall threat detection dashboard."""
    return {
        "total_alerts": 15,
        "critical_alerts": 1,
        "high_alerts": 3,
        "medium_alerts": 6,
        "low_alerts": 5,
        "trends": {
            "alerts_24h": 3,
            "alerts_7d": 12,
            "alerts_30d": 45,
        }
    }
