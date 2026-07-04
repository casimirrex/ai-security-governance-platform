from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.database import get_db
from app.security_modules.audit_logging.service import AuditLoggingService
from app.security_modules.audit_logging.models import AuditLog, ComplianceReport

router = APIRouter()


class AuditLogEntry(BaseModel):
    model_id: int
    action: str
    user: str
    details: dict
    ip_address: str = None


class AuditLogResponse(BaseModel):
    id: int
    timestamp: str
    model_id: int
    action: str
    user: str
    status: str


class ComplianceReportResponse(BaseModel):
    id: int
    model_id: int
    report_type: str
    generated_at: str
    period_start: str
    period_end: str
    findings: list
    status: str


@router.post("/log", response_model=AuditLogResponse)
def create_audit_log(entry: AuditLogEntry, db: Session = Depends(get_db)):
    """Create an audit log entry."""
    service = AuditLoggingService()
    audit_log = service.log_action(
        db,
        entry.model_id,
        entry.action,
        entry.user,
        entry.details,
        entry.ip_address,
    )

    return AuditLogResponse(
        id=audit_log.id,
        timestamp=audit_log.timestamp.isoformat(),
        model_id=audit_log.model_id,
        action=audit_log.action,
        user=audit_log.user,
        status=audit_log.status,
    )


@router.get("/logs/{model_id}")
def get_audit_logs(model_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Get audit logs for a model."""
    service = AuditLoggingService()
    logs = service.get_audit_logs(db, model_id, days)

    from_date = (datetime.now() - timedelta(days=days)).isoformat()

    return {
        "model_id": model_id,
        "period_days": days,
        "from_date": from_date,
        "log_count": len(logs),
        "logs": [
            {
                "log_id": log.id,
                "timestamp": log.timestamp.isoformat(),
                "action": log.action,
                "user": log.user,
                "details": log.details,
            }
            for log in logs
        ]
    }


@router.post("/compliance-report/{model_id}", response_model=ComplianceReportResponse)
def generate_compliance_report(
    model_id: int,
    period_days: int = 30,
    db: Session = Depends(get_db)
):
    """Generate a compliance report from audit logs."""
    service = AuditLoggingService()
    report = service.generate_compliance_report(db, model_id, period_days)

    return ComplianceReportResponse(
        id=report.id,
        model_id=report.model_id,
        report_type=report.report_type,
        generated_at=report.generated_at.isoformat(),
        period_start=report.period_start.isoformat(),
        period_end=report.period_end.isoformat(),
        findings=report.findings or [],
        status=report.status,
    )


@router.get("/compliance-reports/{model_id}")
def get_compliance_reports(model_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get recent compliance reports for a model."""
    service = AuditLoggingService()
    reports = service.get_compliance_reports(db, model_id, limit)

    return {
        "model_id": model_id,
        "report_count": len(reports),
        "reports": [
            {
                "report_id": r.id,
                "type": r.report_type,
                "generated_at": r.generated_at.isoformat(),
                "status": r.status,
            }
            for r in reports
        ]
    }
