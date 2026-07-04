from fastapi import APIRouter
from .endpoints import (
    risk_assessment,
    compliance,
    data_privacy,
    threat_detection,
    audit_logging
)

api_router = APIRouter()

api_router.include_router(
    risk_assessment.router,
    prefix="/risk-assessment",
    tags=["Risk Assessment"]
)
api_router.include_router(
    compliance.router,
    prefix="/compliance",
    tags=["Compliance"]
)
api_router.include_router(
    data_privacy.router,
    prefix="/data-privacy",
    tags=["Data Privacy"]
)
api_router.include_router(
    threat_detection.router,
    prefix="/threat-detection",
    tags=["Threat Detection"]
)
api_router.include_router(
    audit_logging.router,
    prefix="/audit",
    tags=["Audit Logging"]
)
