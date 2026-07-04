import pytest
from app.security_modules.data_privacy.service import DataPrivacyService


class TestDataPrivacyService:

    def test_detect_email_pii(self):
        """Test email PII detection."""
        service = DataPrivacyService()
        data = "Contact admin@example.com for help"

        findings = service.detect_pii(data)
        assert len(findings) > 0
        assert any(f["type"] == "EMAIL" for f in findings)

    def test_detect_phone_pii(self):
        """Test phone number PII detection."""
        service = DataPrivacyService()
        data = "Call me at 555-123-4567"

        findings = service.detect_pii(data)
        assert len(findings) > 0
        assert any(f["type"] == "PHONE" for f in findings)

    def test_detect_ssn_pii(self):
        """Test SSN PII detection."""
        service = DataPrivacyService()
        data = "SSN is 123-45-6789"

        findings = service.detect_pii(data)
        assert len(findings) > 0
        assert any(f["type"] == "SSN" for f in findings)

    def test_detect_credit_card_pii(self):
        """Test credit card PII detection."""
        service = DataPrivacyService()
        data = "Card 1234-5678-9012-3456"

        findings = service.detect_pii(data)
        assert len(findings) > 0
        assert any(f["type"] == "CREDIT_CARD" for f in findings)

    def test_mask_pii(self):
        """Test PII masking."""
        service = DataPrivacyService()
        data = "Email is test@example.com"

        masked = service.mask_pii(data)
        assert "EMAIL_MASKED" in masked
        assert "test@example.com" not in masked

    def test_no_pii_detected(self):
        """Test when no PII is present."""
        service = DataPrivacyService()
        data = "This is normal text without any sensitive information"

        findings = service.detect_pii(data)
        assert len(findings) == 0

    def test_multiple_pii_types(self):
        """Test detection of multiple PII types."""
        service = DataPrivacyService()
        data = "Contact john@example.com or call 555-123-4567. SSN: 123-45-6789"

        findings = service.detect_pii(data)
        assert len(findings) >= 3
        types = {f["type"] for f in findings}
        assert "EMAIL" in types
        assert "PHONE" in types
        assert "SSN" in types
