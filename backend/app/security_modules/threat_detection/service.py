import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.security_modules.threat_detection.models import SecurityAlert, ThreatIndicator

logger = logging.getLogger(__name__)


class ThreatDetectionService:

    THREAT_SEVERITY_LEVELS = {
        "CRITICAL": 5,
        "HIGH": 4,
        "MEDIUM": 3,
        "LOW": 2,
        "INFO": 1,
    }

    @staticmethod
    def classify_threat_severity(indicators: dict) -> str:
        """Classify threat severity based on indicators."""
        severity_score = 0

        if indicators.get("unusual_predictions"):
            severity_score += 2
        if indicators.get("access_anomaly"):
            severity_score += 2
        if indicators.get("unauthorized_access"):
            severity_score += 3
        if indicators.get("data_exfiltration"):
            severity_score += 4
        if indicators.get("model_poisoning_suspected"):
            severity_score += 5

        if severity_score >= 5:
            return "CRITICAL"
        elif severity_score >= 4:
            return "HIGH"
        elif severity_score >= 3:
            return "MEDIUM"
        elif severity_score >= 2:
            return "LOW"
        else:
            return "INFO"

    def detect_threats(
        self,
        db: Session,
        model_id: int,
        model_metrics: dict
    ) -> list:
        """Detect threats based on model metrics."""
        logger.info(f"Detecting threats for model {model_id}")

        alerts = []
        indicators = []

        # Check for unusual predictions
        if model_metrics.get("prediction_confidence_variance", 0) > 50:
            alerts.append({
                "threat_type": "UNUSUAL_PREDICTION_PATTERN",
                "description": "High variance in prediction confidence detected",
            })
            indicators.append({"indicator": "unusual_predictions", "confidence": 0.85})

        # Check for access anomalies
        if model_metrics.get("unexpected_access_patterns"):
            alerts.append({
                "threat_type": "ACCESS_ANOMALY",
                "description": "Unusual access patterns detected",
            })
            indicators.append({"indicator": "access_anomaly", "confidence": 0.75})

        # Check for potential model poisoning
        if model_metrics.get("data_distribution_shift", 0) > 30:
            alerts.append({
                "threat_type": "POTENTIAL_MODEL_POISONING",
                "description": "Significant data distribution shift detected",
            })
            indicators.append({"indicator": "model_poisoning_suspected", "confidence": 0.65})

        # Check for unauthorized access attempts
        if model_metrics.get("failed_auth_attempts", 0) > 10:
            alerts.append({
                "threat_type": "UNAUTHORIZED_ACCESS_ATTEMPT",
                "description": f"{model_metrics['failed_auth_attempts']} failed authentication attempts",
            })
            indicators.append({"indicator": "unauthorized_access", "confidence": 0.90})

        # Create security alerts
        for alert in alerts:
            severity = self.classify_threat_severity({k: True for k in [a["threat_type"] for a in alerts]})
            security_alert = SecurityAlert(
                model_id=model_id,
                threat_type=alert["threat_type"],
                severity=severity,
                description=alert["description"],
                status="OPEN",
                details=alert,
            )
            db.add(security_alert)

        # Create threat indicators
        for indicator in indicators:
            threat_indicator = ThreatIndicator(
                model_id=model_id,
                indicator_type=indicator["indicator"],
                confidence_score=indicator["confidence"],
                details=indicator,
            )
            db.add(threat_indicator)

        db.commit()
        logger.info(f"Threat detection completed. Alerts: {len(alerts)}")
        return alerts
