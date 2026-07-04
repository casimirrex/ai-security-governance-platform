import logging
from sqlalchemy.orm import Session
from .models import ComplianceCheck, ComplianceFramework

logger = logging.getLogger(__name__)


class ComplianceService:

    NIST_AI_RMF_CONTROLS = {
        "AI-1.1": "Purpose and requirements for AI system documented",
        "AI-1.2": "AI system inputs and outputs validated",
        "AI-2.1": "AI model training data quality assured",
        "AI-2.2": "Model versioning and documentation maintained",
        "AI-3.1": "Responsible AI principles implemented",
        "AI-3.2": "Model fairness and bias monitored",
        "AI-4.1": "Data governance policies defined",
        "AI-4.2": "Data access controls enforced",
        "AI-5.1": "Security assessment performed",
        "AI-5.2": "Vulnerability management process established",
    }

    EU_AI_ACT_REQUIREMENTS = {
        "RISK-ASSESSMENT": "High-risk AI systems undergo risk assessment",
        "HUMAN-OVERSIGHT": "Human oversight mechanisms in place",
        "TRANSPARENCY": "Transparency requirements met",
        "DOCUMENTATION": "Technical documentation maintained",
        "MONITORING": "Post-deployment monitoring active",
        "RECORD-KEEPING": "Records of AI system decisions kept",
    }

    @staticmethod
    def check_nist_ai_rmf(model_id: int, model_data: dict) -> dict:
        """Check NIST AI RMF compliance."""
        results = {}
        compliance_score = 0
        total_controls = len(ComplianceService.NIST_AI_RMF_CONTROLS)

        for control_id, control_desc in ComplianceService.NIST_AI_RMF_CONTROLS.items():
            if control_id.startswith("AI-1"):
                passed = model_data.get("documented", False)
            elif control_id.startswith("AI-2"):
                passed = model_data.get("versioning", False)
            elif control_id.startswith("AI-3"):
                passed = model_data.get("responsible_ai", False)
            elif control_id.startswith("AI-4"):
                passed = model_data.get("data_governance", False)
            else:
                passed = model_data.get("security_assessment", False)

            results[control_id] = {"status": "PASS" if passed else "FAIL"}
            if passed:
                compliance_score += 1

        compliance_percentage = (compliance_score / total_controls) * 100
        return {
            "framework": "NIST_AI_RMF",
            "controls_passed": compliance_score,
            "total_controls": total_controls,
            "compliance_score": compliance_percentage,
            "results": results,
        }

    @staticmethod
    def check_eu_ai_act(model_id: int, model_data: dict) -> dict:
        """Check EU AI Act compliance."""
        results = {}
        compliance_score = 0
        total_requirements = len(ComplianceService.EU_AI_ACT_REQUIREMENTS)

        for req_id, req_desc in ComplianceService.EU_AI_ACT_REQUIREMENTS.items():
            passed = False

            if req_id == "RISK-ASSESSMENT":
                passed = model_data.get("risk_assessed", False)
            elif req_id == "HUMAN-OVERSIGHT":
                passed = model_data.get("human_oversight", False)
            elif req_id == "TRANSPARENCY":
                passed = model_data.get("transparency_policy", False)
            elif req_id == "DOCUMENTATION":
                passed = model_data.get("technical_docs", False)
            elif req_id == "MONITORING":
                passed = model_data.get("monitoring_active", False)
            elif req_id == "RECORD-KEEPING":
                passed = model_data.get("audit_logging", False)

            results[req_id] = {"status": "PASS" if passed else "FAIL"}
            if passed:
                compliance_score += 1

        compliance_percentage = (compliance_score / total_requirements) * 100
        return {
            "framework": "EU_AI_ACT",
            "requirements_met": compliance_score,
            "total_requirements": total_requirements,
            "compliance_score": compliance_percentage,
            "results": results,
        }

    def perform_compliance_audit(
        self,
        db: Session,
        model_id: int,
        model_data: dict
    ) -> dict:
        """Perform comprehensive compliance audit."""
        logger.info(f"Starting compliance audit for model {model_id}")

        nist_results = self.check_nist_ai_rmf(model_id, model_data)
        eu_results = self.check_eu_ai_act(model_id, model_data)

        overall_compliance = (
            nist_results["compliance_score"] +
            eu_results["compliance_score"]
        ) / 2

        return {
            "model_id": model_id,
            "overall_compliance_score": overall_compliance,
            "nist_ai_rmf": nist_results,
            "eu_ai_act": eu_results,
            "timestamp": str(__import__("datetime").datetime.now()),
        }
