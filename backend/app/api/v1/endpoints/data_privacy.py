from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.security_modules.data_privacy.service import DataPrivacyService

router = APIRouter()


class DataPrivacyInput(BaseModel):
    model_id: int
    sample_data: dict = {}
    has_pii_detection: bool = False
    pii_masking_enabled: bool = False
    data_classification_done: bool = False
    access_controls_enforced: bool = False
    retention_policy_defined: bool = False


class DataPrivacyResponse(BaseModel):
    id: int
    model_id: int
    pii_detected: int
    pii_masked: int
    privacy_score: float
    findings: list


@router.post("/assess", response_model=DataPrivacyResponse)
def assess_data_privacy(
    privacy_input: DataPrivacyInput,
    db: Session = Depends(get_db)
):
    """Assess data privacy and PII protection measures."""
    service = DataPrivacyService()
    assessment = service.perform_privacy_assessment(
        db,
        privacy_input.model_id,
        privacy_input.sample_data if privacy_input.sample_data else {}
    )

    return DataPrivacyResponse(
        id=assessment.id,
        model_id=assessment.model_id,
        pii_detected=assessment.pii_detected,
        pii_masked=assessment.pii_masked,
        privacy_score=assessment.privacy_score,
        findings=assessment.findings or [],
    )


@router.get("/pii-patterns")
def get_pii_patterns():
    """Get common PII patterns for detection."""
    return {
        "patterns": [
            {"type": "EMAIL", "description": "Email addresses"},
            {"type": "PHONE", "description": "Phone numbers"},
            {"type": "SSN", "description": "Social Security Numbers"},
            {"type": "CREDIT_CARD", "description": "Credit card numbers"},
            {"type": "IP_ADDRESS", "description": "IP addresses"},
        ]
    }
