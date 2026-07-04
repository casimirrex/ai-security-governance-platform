from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from security_modules.compliance.service import ComplianceService
from pydantic import BaseModel

router = APIRouter()


class ComplianceData(BaseModel):
    model_id: int
    documented: bool = False
    versioning: bool = False
    responsible_ai: bool = False
    data_governance: bool = False
    security_assessment: bool = False
    risk_assessed: bool = False
    human_oversight: bool = False
    transparency_policy: bool = False
    technical_docs: bool = False
    monitoring_active: bool = False
    audit_logging: bool = False


@router.post("/audit")
def audit_compliance(
    compliance_data: ComplianceData,
    db: Session = Depends(get_db)
):
    """Perform AI compliance audit against NIST AI RMF and EU AI Act."""
    service = ComplianceService()
    results = service.perform_compliance_audit(
        db,
        compliance_data.model_id,
        compliance_data.dict()
    )
    return results


@router.get("/frameworks")
def list_compliance_frameworks():
    """List available compliance frameworks."""
    return {
        "frameworks": [
            {"name": "NIST AI RMF", "description": "NIST AI Risk Management Framework"},
            {"name": "EU AI Act", "description": "European Union AI Act"},
            {"name": "ISO/IEC 42001", "description": "AI Management Systems"},
        ]
    }
