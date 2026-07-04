import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.security_modules.audit_logging.models import AuditLog, ComplianceReport

logger = logging.getLogger(__name__)


class AuditLoggingService:

    @staticmethod
    def log_action(
        db: Session,
        model_id: int,
        action: str,
        user: str,
        details: dict,
        ip_address: str = None,
    ) -> AuditLog:
        """Log a security action for audit trail."""
        audit_entry = AuditLog(
            model_id=model_id,
            action=action,
            user=user,
            details=details,
            ip_address=ip_address,
            status="LOGGED",
        )
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)

        logger.info(f"Audit log created: {action} by {user} for model {model_id}")
        return audit_entry

    @staticmethod
    def get_audit_logs(
        db: Session,
        model_id: int,
        days: int = 30,
    ) -> list:
        """Retrieve audit logs for a model."""
        from_date = datetime.now() - timedelta(days=days)

        logs = db.query(AuditLog).filter(
            AuditLog.model_id == model_id,
            AuditLog.timestamp >= from_date,
        ).order_by(AuditLog.timestamp.desc()).all()

        return logs

    @staticmethod
    def generate_compliance_report(
        db: Session,
        model_id: int,
        period_days: int = 30,
    ) -> ComplianceReport:
        """Generate a compliance report from audit logs."""
        from_date = datetime.now() - timedelta(days=period_days)
        to_date = datetime.now()

        audit_logs = db.query(AuditLog).filter(
            AuditLog.model_id == model_id,
            AuditLog.timestamp >= from_date,
            AuditLog.timestamp <= to_date,
        ).all()

        findings = []
        compliance_issues = 0

        # Analyze logs for compliance
        for log in audit_logs:
            if log.status == "FAILED":
                findings.append({
                    "issue": log.action,
                    "timestamp": log.timestamp.isoformat(),
                    "user": log.user,
                })
                compliance_issues += 1

        # Create compliance report
        report = ComplianceReport(
            model_id=model_id,
            report_type="COMPLIANCE_AUDIT",
            period_start=from_date,
            period_end=to_date,
            findings=findings,
            status="COMPLIANT" if compliance_issues == 0 else "NON_COMPLIANT",
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        logger.info(f"Compliance report generated for model {model_id}")
        return report

    @staticmethod
    def get_compliance_reports(
        db: Session,
        model_id: int,
        limit: int = 10,
    ) -> list:
        """Get recent compliance reports for a model."""
        reports = db.query(ComplianceReport).filter(
            ComplianceReport.model_id == model_id,
        ).order_by(ComplianceReport.generated_at.desc()).limit(limit).all()

        return reports
