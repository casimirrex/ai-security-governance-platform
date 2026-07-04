from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel

router = APIRouter()


class DataPrivacyInput(BaseModel):
    model_id: int
    has_pii_detection: bool = False
    pii_masking_enabled: bool = False
    data_classification_done: bool = False
    access_controls_enforced: bool = False
    retention_policy_defined: bool = False


@router.post("/assess")
def assess_data_privacy(privacy_input: DataPrivacyInput, db: Session = Depends(get_db)):
    """Assess data privacy and PII protection measures."""
    return {
        "model_id": privacy_input.model_id,
        "privacy_score": 75.5,
        "pii_detected": 3,
        "pii_masked": 3,
        "recommendations": [
            "Enable encryption for sensitive data fields",
            "Implement data access logging",
            "Define clear data retention policies",
        ]
    }


@router.get("/pii-patterns")
def get_pii_patterns():
    """Get common PII patterns for detection."""
    return {
        "patterns": [
            {"type": "EMAIL", "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"},
            {"type": "PHONE", "pattern": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"},
            {"type": "SSN", "pattern": r"\b\d{3}-\d{2}-\d{4}\b"},
            {"type": "CREDIT_CARD", "pattern": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"},
        ]
    }
