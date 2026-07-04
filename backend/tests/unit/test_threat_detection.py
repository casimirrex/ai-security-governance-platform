import pytest
from app.security_modules.threat_detection.service import ThreatDetectionService


class TestThreatDetectionService:

    def test_classify_critical_threat(self):
        """Test classification of critical threats."""
        service = ThreatDetectionService()

        indicators = {
            "data_exfiltration": True,
        }

        severity = service.classify_threat_severity(indicators)
        assert severity == "CRITICAL"

    def test_classify_high_threat(self):
        """Test classification of high threats."""
        service = ThreatDetectionService()

        indicators = {
            "model_poisoning_suspected": True,
            "unauthorized_access": True,
        }

        severity = service.classify_threat_severity(indicators)
        assert severity == "HIGH"

    def test_classify_medium_threat(self):
        """Test classification of medium threats."""
        service = ThreatDetectionService()

        indicators = {
            "unusual_predictions": True,
            "access_anomaly": True,
        }

        severity = service.classify_threat_severity(indicators)
        assert severity == "MEDIUM"

    def test_classify_low_threat(self):
        """Test classification of low threats."""
        service = ThreatDetectionService()

        indicators = {
            "unusual_predictions": True,
        }

        severity = service.classify_threat_severity(indicators)
        assert severity == "LOW"

    def test_classify_no_threat(self):
        """Test classification when no threats detected."""
        service = ThreatDetectionService()

        indicators = {}

        severity = service.classify_threat_severity(indicators)
        assert severity == "INFO"

    def test_severity_level_weights(self):
        """Test that severity levels have correct weights."""
        service = ThreatDetectionService()

        assert ThreatDetectionService.THREAT_SEVERITY_LEVELS["CRITICAL"] == 5
        assert ThreatDetectionService.THREAT_SEVERITY_LEVELS["HIGH"] == 4
        assert ThreatDetectionService.THREAT_SEVERITY_LEVELS["MEDIUM"] == 3
        assert ThreatDetectionService.THREAT_SEVERITY_LEVELS["LOW"] == 2
        assert ThreatDetectionService.THREAT_SEVERITY_LEVELS["INFO"] == 1
