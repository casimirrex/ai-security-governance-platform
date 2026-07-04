#!/bin/bash

# AI Security Governance Platform - API Testing Script

set -e

API_URL="http://localhost:8000"
echo "==================================="
echo "AI Security Platform - API Test"
echo "==================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "${BLUE}Test 1: Health Check${NC}"
HEALTH=$(curl -s $API_URL/health)
echo "Response: $HEALTH"
echo -e "${GREEN}✓ Health check passed${NC}\n"

# Test 2: Root Endpoint
echo -e "${BLUE}Test 2: Root Endpoint${NC}"
ROOT=$(curl -s $API_URL/)
echo "Response: $ROOT"
echo -e "${GREEN}✓ Root endpoint working${NC}\n"

# Test 3: Register Model
echo -e "${BLUE}Test 3: Register AI Model${NC}"
REGISTER=$(curl -s -X POST $API_URL/api/v1/risk-assessment/register-model \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-model-'"$(date +%s)"'",
    "description": "Test model for security assessment",
    "model_type": "neural_network",
    "framework": "tensorflow",
    "version": "1.0.0"
  }')
echo "Response: $REGISTER"
MODEL_ID=$(echo $REGISTER | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo -e "${GREEN}✓ Model registered with ID: $MODEL_ID${NC}\n"

# Test 4: Perform Risk Assessment
echo -e "${BLUE}Test 4: Perform Security Risk Assessment${NC}"
ASSESSMENT=$(curl -s -X POST $API_URL/api/v1/risk-assessment/assess \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": 1,
    "has_input_validation": true,
    "has_normalization": true,
    "uses_regularization": true,
    "ensemble_methods": false,
    "untrusted_sources": false,
    "has_data_validation": true,
    "data_signed": false,
    "audit_logging": true,
    "public_api": false,
    "rate_limiting": true,
    "authentication": true,
    "downloadable_weights": false,
    "confidence_scores": false,
    "overfitting_detected": false,
    "differential_privacy": false,
    "training_data_public": false,
    "encryption_at_rest": true,
    "pii_masking": true,
    "encryption_in_transit": true,
    "verbose_logging": false
  }')
echo "Response: $ASSESSMENT"
echo -e "${GREEN}✓ Risk assessment completed${NC}\n"

# Test 5: Compliance Audit
echo -e "${BLUE}Test 5: Perform Compliance Audit${NC}"
COMPLIANCE=$(curl -s -X POST $API_URL/api/v1/compliance/audit \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": 1,
    "documented": true,
    "versioning": true,
    "responsible_ai": true,
    "data_governance": true,
    "security_assessment": true,
    "risk_assessed": true,
    "human_oversight": true,
    "transparency_policy": true,
    "technical_docs": true,
    "monitoring_active": true,
    "audit_logging": true
  }')
echo "Response: $COMPLIANCE"
echo -e "${GREEN}✓ Compliance audit completed${NC}\n"

# Test 6: Data Privacy Assessment
echo -e "${BLUE}Test 6: Data Privacy Assessment${NC}"
PRIVACY=$(curl -s -X POST $API_URL/api/v1/data-privacy/assess \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": 1,
    "has_pii_detection": true,
    "pii_masking_enabled": true,
    "data_classification_done": true,
    "access_controls_enforced": true,
    "retention_policy_defined": true
  }')
echo "Response: $PRIVACY"
echo -e "${GREEN}✓ Data privacy assessment completed${NC}\n"

# Test 7: Get PII Patterns
echo -e "${BLUE}Test 7: Get PII Detection Patterns${NC}"
PII=$(curl -s $API_URL/api/v1/data-privacy/pii-patterns)
echo "Response: $PII"
echo -e "${GREEN}✓ PII patterns retrieved${NC}\n"

# Test 8: Threat Detection
echo -e "${BLUE}Test 8: Create Threat Alert${NC}"
THREAT=$(curl -s -X POST $API_URL/api/v1/threat-detection/alert \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": 1,
    "threat_type": "UNUSUAL_PREDICTION_PATTERN",
    "severity": "MEDIUM",
    "description": "Detected unusual prediction confidence distribution"
  }')
echo "Response: $THREAT"
echo -e "${GREEN}✓ Threat alert created${NC}\n"

# Test 9: Get Threat Dashboard
echo -e "${BLUE}Test 9: Threat Detection Dashboard${NC}"
DASHBOARD=$(curl -s $API_URL/api/v1/threat-detection/dashboard)
echo "Response: $DASHBOARD"
echo -e "${GREEN}✓ Threat dashboard retrieved${NC}\n"

# Test 10: Create Audit Log
echo -e "${BLUE}Test 10: Create Audit Log Entry${NC}"
AUDIT=$(curl -s -X POST $API_URL/api/v1/audit/log \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": 1,
    "action": "MODEL_ASSESSMENT",
    "user": "security_admin",
    "details": {"risk_level": "MEDIUM", "score": 72.5}
  }')
echo "Response: $AUDIT"
echo -e "${GREEN}✓ Audit log created${NC}\n"

echo "==================================="
echo -e "${GREEN}All Tests Completed Successfully!${NC}"
echo "==================================="
echo ""
echo "Next Steps:"
echo "1. View API Documentation: http://localhost:8000/docs"
echo "2. View Prometheus Metrics: http://localhost:9090"
echo "3. View Grafana Dashboards: http://localhost:3001"
echo "4. Check backend logs: docker compose logs -f backend"
echo "5. Stop services: docker compose down"
