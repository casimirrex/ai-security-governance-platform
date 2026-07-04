import pytest
from app.security_modules.risk_assessment.service import RiskAssessmentService


class TestRiskAssessmentService:

    def test_assess_adversarial_robustness(self):
        """Test adversarial robustness assessment."""
        service = RiskAssessmentService()

        model_data = {
            "has_input_validation": True,
            "has_normalization": True,
            "uses_regularization": True,
            "ensemble_methods": False,
        }

        score = service.assess_adversarial_robustness(model_data)
        assert 0 <= score <= 100
        assert score == 75.0  # 3/4 factors present

    def test_assess_data_poisoning_risk(self):
        """Test data poisoning risk assessment."""
        service = RiskAssessmentService()

        model_data = {
            "untrusted_sources": True,
            "has_data_validation": True,
            "data_signed": True,
            "audit_logging": True,
        }

        risk = service.assess_data_poisoning_risk(model_data)
        assert 0 <= risk <= 100

    def test_assess_model_stealing_risk(self):
        """Test model stealing risk assessment."""
        service = RiskAssessmentService()

        model_data = {
            "public_api": False,
            "rate_limiting": True,
            "authentication": True,
            "downloadable_weights": False,
        }

        risk = service.assess_model_stealing_risk(model_data)
        assert 0 <= risk <= 100
        assert risk == 0.0  # All protective measures in place

    def test_calculate_overall_risk_score(self):
        """Test overall risk score calculation."""
        service = RiskAssessmentService()

        score, level = service.calculate_overall_risk_score(
            adversarial=80,
            poisoning=70,
            stealing=60,
            membership=50,
            privacy=40,
        )

        assert 0 <= score <= 100
        assert level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    def test_generate_findings(self):
        """Test findings generation."""
        service = RiskAssessmentService()

        scores = {
            "adversarial": 40,
            "poisoning": 80,
            "stealing": 60,
            "membership": 50,
            "privacy": 70,
        }

        findings = service.generate_findings({}, scores)
        assert isinstance(findings, list)
        assert len(findings) > 0
        assert all("type" in f and "severity" in f for f in findings)

    def test_generate_recommendations(self):
        """Test recommendations generation."""
        service = RiskAssessmentService()

        findings = [
            {
                "type": "LOW_ADVERSARIAL_ROBUSTNESS",
                "severity": "HIGH",
                "description": "Test",
            }
        ]

        recommendations = service.generate_recommendations(findings)
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all("finding" in r and "actions" in r for r in recommendations)
