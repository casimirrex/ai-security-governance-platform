import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from security_modules.risk_assessment.service import RiskAssessmentService
from security_modules.risk_assessment.models import SecurityRiskAssessment, AIModel
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)


class ModelInput(BaseModel):
    name: str
    description: str
    model_type: str
    framework: str
    version: str


class ModelSecurityData(BaseModel):
    model_id: int
    has_input_validation: bool = False
    has_normalization: bool = False
    uses_regularization: bool = False
    ensemble_methods: bool = False
    untrusted_sources: bool = False
    has_data_validation: bool = True
    data_signed: bool = False
    audit_logging: bool = False
    public_api: bool = False
    rate_limiting: bool = False
    authentication: bool = False
    downloadable_weights: bool = False
    confidence_scores: bool = False
    overfitting_detected: bool = False
    differential_privacy: bool = False
    training_data_public: bool = False
    encryption_at_rest: bool = False
    pii_masking: bool = False
    encryption_in_transit: bool = False
    verbose_logging: bool = False


class RiskAssessmentResponse(BaseModel):
    id: int
    model_id: int
    adversarial_robustness_score: float
    data_poisoning_risk: float
    model_stealing_risk: float
    membership_inference_risk: float
    privacy_leakage_risk: float
    overall_risk_score: float
    risk_level: str
    findings: list
    recommendations: list


@router.post("/register-model", status_code=status.HTTP_201_CREATED)
def register_model(model: ModelInput, db: Session = Depends(get_db)):
    """Register an AI model for security assessment."""
    existing_model = db.query(AIModel).filter(
        AIModel.name == model.name
    ).first()

    if existing_model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model with this name already exists"
        )

    new_model = AIModel(
        name=model.name,
        description=model.description,
        model_type=model.model_type,
        framework=model.framework,
        version=model.version,
    )

    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    logger.info(f"Model registered: {new_model.id} - {new_model.name}")
    return {"id": new_model.id, "name": new_model.name, "message": "Model registered successfully"}


@router.post("/assess", response_model=RiskAssessmentResponse)
def assess_model_security(
    security_data: ModelSecurityData,
    db: Session = Depends(get_db)
):
    """Perform security risk assessment on registered AI model."""
    model = db.query(AIModel).filter(
        AIModel.id == security_data.model_id
    ).first()

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )

    service = RiskAssessmentService()
    model_data = security_data.dict()

    assessment = service.perform_assessment(db, security_data.model_id, model_data)

    return RiskAssessmentResponse(
        id=assessment.id,
        model_id=assessment.model_id,
        adversarial_robustness_score=assessment.adversarial_robustness_score,
        data_poisoning_risk=assessment.data_poisoning_risk,
        model_stealing_risk=assessment.model_stealing_risk,
        membership_inference_risk=assessment.membership_inference_risk,
        privacy_leakage_risk=assessment.privacy_leakage_risk,
        overall_risk_score=assessment.overall_risk_score,
        risk_level=assessment.risk_level,
        findings=assessment.findings,
        recommendations=assessment.recommendations,
    )


@router.get("/assessment/{assessment_id}", response_model=RiskAssessmentResponse)
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific risk assessment."""
    assessment = db.query(SecurityRiskAssessment).filter(
        SecurityRiskAssessment.id == assessment_id
    ).first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    return RiskAssessmentResponse(
        id=assessment.id,
        model_id=assessment.model_id,
        adversarial_robustness_score=assessment.adversarial_robustness_score,
        data_poisoning_risk=assessment.data_poisoning_risk,
        model_stealing_risk=assessment.model_stealing_risk,
        membership_inference_risk=assessment.membership_inference_risk,
        privacy_leakage_risk=assessment.privacy_leakage_risk,
        overall_risk_score=assessment.overall_risk_score,
        risk_level=assessment.risk_level,
        findings=assessment.findings,
        recommendations=assessment.recommendations,
    )


@router.get("/model/{model_id}/assessments")
def get_model_assessments(model_id: int, db: Session = Depends(get_db)):
    """Get all assessments for a specific model."""
    assessments = db.query(SecurityRiskAssessment).filter(
        SecurityRiskAssessment.model_id == model_id
    ).all()

    if not assessments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No assessments found for this model"
        )

    return {
        "model_id": model_id,
        "assessment_count": len(assessments),
        "assessments": [
            {
                "id": a.id,
                "assessment_date": a.assessment_date,
                "risk_level": a.risk_level,
                "overall_risk_score": a.overall_risk_score,
            }
            for a in assessments
        ]
    }
