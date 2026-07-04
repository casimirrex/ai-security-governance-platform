import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.security_modules.risk_assessment.models import SecurityRiskAssessment, VulnerabilityFinding, AIModel

logger = logging.getLogger(__name__)


class RiskAssessmentService:

    @staticmethod
    def assess_adversarial_robustness(model_data: dict) -> float:
        """
        Assess model's robustness against adversarial attacks.
        Returns score 0-100 (higher is better).
        """
        robustness_factors = {
            "input_validation": model_data.get("has_input_validation", False),
            "normalization": model_data.get("has_normalization", False),
            "regularization": model_data.get("uses_regularization", False),
            "ensemble": model_data.get("ensemble_methods", False),
        }

        score = sum(robustness_factors.values()) * 25
        logger.info(f"Adversarial robustness score: {score}")
        return float(score)

    @staticmethod
    def assess_data_poisoning_risk(model_data: dict) -> float:
        """
        Assess risk of data poisoning attacks.
        Returns risk score 0-100 (higher is worse).
        """
        risk_factors = {
            "untrusted_data_sources": model_data.get("untrusted_sources", False),
            "no_data_validation": not model_data.get("has_data_validation", True),
            "no_data_signing": not model_data.get("data_signed", False),
            "no_audit_logging": not model_data.get("audit_logging", False),
        }

        risk_score = sum(risk_factors.values()) * 25
        logger.info(f"Data poisoning risk: {risk_score}")
        return float(risk_score)

    @staticmethod
    def assess_model_stealing_risk(model_data: dict) -> float:
        """
        Assess risk of model extraction/stealing.
        Returns risk score 0-100 (higher is worse).
        """
        risk_factors = {
            "exposed_api": model_data.get("public_api", False),
            "no_rate_limiting": not model_data.get("rate_limiting", False),
            "no_authentication": not model_data.get("authentication", False),
            "downloadable_weights": model_data.get("downloadable_weights", False),
        }

        risk_score = sum(risk_factors.values()) * 25
        logger.info(f"Model stealing risk: {risk_score}")
        return float(risk_score)

    @staticmethod
    def assess_membership_inference_risk(model_data: dict) -> float:
        """
        Assess risk of membership inference attacks.
        Returns risk score 0-100 (higher is worse).
        """
        risk_factors = {
            "high_confidence_outputs": model_data.get("confidence_scores", False),
            "overfitting": model_data.get("overfitting_detected", False),
            "no_differential_privacy": not model_data.get("differential_privacy", False),
            "training_data_exposed": model_data.get("training_data_public", False),
        }

        risk_score = sum(risk_factors.values()) * 25
        logger.info(f"Membership inference risk: {risk_score}")
        return float(risk_score)

    @staticmethod
    def assess_privacy_leakage_risk(model_data: dict) -> float:
        """
        Assess risk of training data leakage via model outputs.
        Returns risk score 0-100 (higher is worse).
        """
        risk_factors = {
            "unencrypted_data": not model_data.get("encryption_at_rest", False),
            "no_pii_masking": not model_data.get("pii_masking", False),
            "insecure_transmission": not model_data.get("encryption_in_transit", False),
            "excessive_logging": model_data.get("verbose_logging", False),
        }

        risk_score = sum(risk_factors.values()) * 25
        logger.info(f"Privacy leakage risk: {risk_score}")
        return float(risk_score)

    @staticmethod
    def calculate_overall_risk_score(
        adversarial: float,
        poisoning: float,
        stealing: float,
        membership: float,
        privacy: float
    ) -> tuple[float, str]:
        """
        Calculate weighted overall risk score.
        Returns (score, risk_level)
        """
        weights = {
            "adversarial": 0.20,
            "poisoning": 0.25,
            "stealing": 0.20,
            "membership": 0.15,
            "privacy": 0.20,
        }

        overall_score = (
            (100 - adversarial) * weights["adversarial"] +
            (100 - poisoning) * weights["poisoning"] +
            (100 - stealing) * weights["stealing"] +
            (100 - membership) * weights["membership"] +
            (100 - privacy) * weights["privacy"]
        )

        if overall_score >= 80:
            risk_level = "LOW"
        elif overall_score >= 60:
            risk_level = "MEDIUM"
        elif overall_score >= 40:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"

        return float(overall_score), risk_level

    @staticmethod
    def generate_findings(model_data: dict, scores: dict) -> list:
        """
        Generate security findings based on risk scores.
        """
        findings = []

        if scores["adversarial"] < 60:
            findings.append({
                "type": "LOW_ADVERSARIAL_ROBUSTNESS",
                "severity": "HIGH",
                "description": "Model lacks sufficient defenses against adversarial attacks",
            })

        if scores["poisoning"] > 40:
            findings.append({
                "type": "DATA_POISONING_RISK",
                "severity": "CRITICAL" if scores["poisoning"] > 75 else "HIGH",
                "description": "Model training pipeline vulnerable to data poisoning",
            })

        if scores["stealing"] > 50:
            findings.append({
                "type": "MODEL_EXTRACTION_RISK",
                "severity": "HIGH",
                "description": "Model API/deployment may expose model architecture",
            })

        if scores["membership"] > 45:
            findings.append({
                "type": "MEMBERSHIP_INFERENCE_RISK",
                "severity": "MEDIUM",
                "description": "Model outputs may leak training data information",
            })

        if scores["privacy"] > 55:
            findings.append({
                "type": "PRIVACY_LEAKAGE_RISK",
                "severity": "HIGH",
                "description": "Data protection controls insufficient",
            })

        return findings

    @staticmethod
    def generate_recommendations(findings: list) -> list:
        """
        Generate remediation recommendations based on findings.
        """
        recommendations = []

        for finding in findings:
            if finding["type"] == "LOW_ADVERSARIAL_ROBUSTNESS":
                recommendations.append({
                    "finding": finding["type"],
                    "actions": [
                        "Implement input validation and sanitization",
                        "Add adversarial training to model training pipeline",
                        "Deploy model robustness testing before production",
                    ]
                })
            elif finding["type"] == "DATA_POISONING_RISK":
                recommendations.append({
                    "finding": finding["type"],
                    "actions": [
                        "Implement data validation and integrity checks",
                        "Use digital signatures for training data",
                        "Enable audit logging for data ingestion",
                        "Restrict data sources to trusted origins",
                    ]
                })
            elif finding["type"] == "MODEL_EXTRACTION_RISK":
                recommendations.append({
                    "finding": finding["type"],
                    "actions": [
                        "Implement rate limiting on model API",
                        "Add authentication and authorization",
                        "Use prediction confidence thresholding",
                        "Monitor for suspicious query patterns",
                    ]
                })
            elif finding["type"] == "MEMBERSHIP_INFERENCE_RISK":
                recommendations.append({
                    "finding": finding["type"],
                    "actions": [
                        "Implement differential privacy",
                        "Add noise to model predictions",
                        "Reduce model confidence in outputs",
                        "Monitor model performance for overfitting",
                    ]
                })
            elif finding["type"] == "PRIVACY_LEAKAGE_RISK":
                recommendations.append({
                    "finding": finding["type"],
                    "actions": [
                        "Enable encryption at rest and in transit",
                        "Implement PII masking and redaction",
                        "Restrict data access with RBAC",
                        "Monitor data access logs",
                    ]
                })

        return recommendations

    def perform_assessment(
        self,
        db: Session,
        model_id: int,
        model_data: dict
    ) -> SecurityRiskAssessment:
        """
        Perform complete security risk assessment on AI model.
        """
        logger.info(f"Starting security assessment for model {model_id}")

        adversarial = self.assess_adversarial_robustness(model_data)
        poisoning = self.assess_data_poisoning_risk(model_data)
        stealing = self.assess_model_stealing_risk(model_data)
        membership = self.assess_membership_inference_risk(model_data)
        privacy = self.assess_privacy_leakage_risk(model_data)

        overall_score, risk_level = self.calculate_overall_risk_score(
            adversarial, poisoning, stealing, membership, privacy
        )

        scores = {
            "adversarial": adversarial,
            "poisoning": poisoning,
            "stealing": stealing,
            "membership": membership,
            "privacy": privacy,
        }

        findings = self.generate_findings(model_data, scores)
        recommendations = self.generate_recommendations(findings)

        assessment = SecurityRiskAssessment(
            model_id=model_id,
            adversarial_robustness_score=adversarial,
            data_poisoning_risk=poisoning,
            model_stealing_risk=stealing,
            membership_inference_risk=membership,
            privacy_leakage_risk=privacy,
            overall_risk_score=overall_score,
            risk_level=risk_level,
            findings=findings,
            recommendations=recommendations,
            status="completed"
        )

        db.add(assessment)
        db.commit()
        db.refresh(assessment)

        logger.info(f"Assessment completed. Risk level: {risk_level}, Score: {overall_score}")
        return assessment
