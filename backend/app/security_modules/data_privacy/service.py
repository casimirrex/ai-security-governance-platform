import logging
import re
from sqlalchemy.orm import Session
from app.security_modules.data_privacy.models import DataPrivacyAssessment, PIIRecord

logger = logging.getLogger(__name__)


class DataPrivacyService:

    PII_PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "PHONE": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        "IP_ADDRESS": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    }

    @staticmethod
    def detect_pii(data: str) -> list:
        """Detect PII in data using regex patterns."""
        findings = []
        for pii_type, pattern in DataPrivacyService.PII_PATTERNS.items():
            matches = re.finditer(pattern, str(data))
            for match in matches:
                findings.append({
                    "type": pii_type,
                    "value": match.group(),
                    "position": match.start(),
                })
        return findings

    @staticmethod
    def mask_pii(data: str) -> str:
        """Mask PII in data."""
        masked = data
        for pii_type, pattern in DataPrivacyService.PII_PATTERNS.items():
            masked = re.sub(pattern, f"[{pii_type}_MASKED]", masked)
        return masked

    def perform_privacy_assessment(
        self,
        db: Session,
        model_id: int,
        data: dict
    ) -> DataPrivacyAssessment:
        """Perform comprehensive data privacy assessment."""
        logger.info(f"Starting privacy assessment for model {model_id}")

        pii_detected = 0
        pii_masked = 0
        findings = []

        for key, value in data.items():
            pii_findings = self.detect_pii(str(value))
            pii_detected += len(pii_findings)
            if pii_findings:
                findings.append({
                    "field": key,
                    "findings": pii_findings,
                })
                pii_masked += len(pii_findings)

        privacy_score = 100 - (pii_detected * 10) if pii_detected < 10 else 0
        privacy_score = max(0, privacy_score)

        assessment = DataPrivacyAssessment(
            model_id=model_id,
            pii_detected=pii_detected,
            pii_masked=pii_masked,
            privacy_score=privacy_score,
            findings=findings,
        )

        db.add(assessment)
        db.commit()
        db.refresh(assessment)

        logger.info(f"Privacy assessment completed. PII detected: {pii_detected}")
        return assessment
