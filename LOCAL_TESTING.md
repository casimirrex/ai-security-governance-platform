# Local Testing Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites Check
```bash
# Verify you have:
git --version          # Git 2.0+
docker --version       # Docker 20+
docker compose version # Docker Compose v2+
python3 --version      # Python 3.11+
```

### Run Everything in 4 Commands

```bash
# 1. Clone the repo
git clone https://github.com/casimirrex/ai-security-governance-platform.git
cd ai-security-governance-platform

# 2. Copy environment file
cp .env.example .env

# 3. Start all services
docker compose up -d

# 4. Wait and test
sleep 30
curl http://localhost:8000/health
```

---

## 📝 Detailed Step-by-Step Guide

### **Step 1: Clone Repository**

```bash
# Create a working directory
mkdir ~/dev-projects
cd ~/dev-projects

# Clone the GitHub repository
git clone https://github.com/casimirrex/ai-security-governance-platform.git
cd ai-security-governance-platform

# Verify structure
ls -la
# You should see:
# - README.md
# - docker-compose.yml
# - backend/
# - azure-infrastructure/
# - docs/
```

### **Step 2: Set Up Environment**

```bash
# Copy environment template
cp .env.example .env

# View the configuration (no need to edit for local testing)
cat .env

# The defaults are:
# - Database: PostgreSQL on localhost:5432
# - Cache: Redis on localhost:6379
# - API: http://localhost:8000
# - Environment: development
```

### **Step 3: Start Docker Services**

```bash
# Start all services in background
docker compose up -d

# Monitor startup (this will show live logs)
docker compose logs -f backend

# Wait for "Uvicorn running on http://0.0.0.0:8000" message
# Then press Ctrl+C to exit logs
```

### **Step 4: Verify Services**

```bash
# Check all services are running
docker compose ps

# Expected output:
# NAME              IMAGE           STATUS
# ai-security-db   postgres        Up (healthy)
# ai-security-cache redis          Up (healthy)
# ai-security-backend FastAPI      Up (healthy)
# ai-security-prometheus            Up
# ai-security-grafana              Up
```

### **Step 5: Test Health Check**

```bash
# Basic health check
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","app":"AI Security Governance Platform"}
```

### **Step 6: View API Documentation**

```bash
# Open in browser (interactive API documentation)
open http://localhost:8000/docs

# Alternative URLs:
# - OpenAPI JSON: http://localhost:8000/openapi.json
# - ReDoc: http://localhost:8000/redoc
```

### **Step 7: Run Complete API Test**

```bash
# Run the automated test script
bash test-api.sh

# This will:
# ✓ Test health endpoint
# ✓ Register a model
# ✓ Perform risk assessment
# ✓ Audit compliance
# ✓ Assess data privacy
# ✓ Test threat detection
# ✓ Create audit logs
# ✓ Show all API responses
```

### **Step 8: Manual API Testing**

#### **Test 1: Register a Model**
```bash
curl -X POST http://localhost:8000/api/v1/risk-assessment/register-model \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-ai-model-v1",
    "description": "Production ML model",
    "model_type": "neural_network",
    "framework": "tensorflow",
    "version": "1.0.0"
  }'

# Response:
# {
#   "id": 1,
#   "name": "my-ai-model-v1",
#   "message": "Model registered successfully"
# }
```

#### **Test 2: Risk Assessment**
```bash
curl -X POST http://localhost:8000/api/v1/risk-assessment/assess \
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
  }'

# Response includes:
# {
#   "id": 1,
#   "model_id": 1,
#   "overall_risk_score": 78.5,
#   "risk_level": "LOW",
#   "findings": [...],
#   "recommendations": [...]
# }
```

#### **Test 3: Compliance Audit**
```bash
curl -X POST http://localhost:8000/api/v1/compliance/audit \
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
  }'

# Response:
# {
#   "model_id": 1,
#   "overall_compliance_score": 85.5,
#   "nist_ai_rmf": {...},
#   "eu_ai_act": {...}
# }
```

#### **Test 4: Data Privacy**
```bash
curl -X POST http://localhost:8000/api/v1/data-privacy/assess \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": 1,
    "has_pii_detection": true,
    "pii_masking_enabled": true,
    "data_classification_done": true,
    "access_controls_enforced": true,
    "retention_policy_defined": true
  }'
```

#### **Test 5: Threat Detection**
```bash
curl -X POST http://localhost:8000/api/v1/threat-detection/alert \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": 1,
    "threat_type": "UNUSUAL_PREDICTION_PATTERN",
    "severity": "MEDIUM",
    "description": "Detected unusual confidence distribution"
  }'
```

### **Step 9: View Monitoring Dashboards**

```bash
# Prometheus (metrics collection)
open http://localhost:9090
# Query: rate(requests_total[5m])

# Grafana (visualization)
open http://localhost:3001
# Default login: admin / admin
# Dashboards show API metrics, database performance, etc.
```

### **Step 10: Check Database**

```bash
# Connect to PostgreSQL container
docker compose exec postgres psql -U postgres -d ai_security_db

# Inside psql:
# List tables
\dt

# View models
SELECT * FROM ai_models;

# View assessments
SELECT id, model_id, risk_level, overall_risk_score FROM security_risk_assessments;

# Exit psql
\q
```

### **Step 11: View Backend Logs**

```bash
# Real-time logs
docker compose logs -f backend

# Specific service logs
docker compose logs postgres     # Database logs
docker compose logs redis        # Cache logs

# Follow specific number of lines
docker compose logs --tail 50 backend
```

### **Step 12: Stop Services**

```bash
# Stop all services
docker compose down

# Remove volumes too (clean slate)
docker compose down -v

# View stopped containers
docker compose ps -a
```

---

## 🎯 What You're Testing

### **Core Functionality**
✅ **API Server**: FastAPI application with 5 security modules  
✅ **Database**: PostgreSQL with proper schema and relationships  
✅ **Cache**: Redis for performance optimization  
✅ **Monitoring**: Prometheus + Grafana metrics collection  

### **Security Modules**
✅ **Risk Assessment**: AI model vulnerability scoring  
✅ **Compliance**: NIST AI RMF and EU AI Act checks  
✅ **Data Privacy**: PII detection and classification  
✅ **Threat Detection**: Real-time security alerts  
✅ **Audit Logging**: Comprehensive audit trails  

### **Performance**
✅ Health check: < 100ms  
✅ Risk assessment: < 5s  
✅ Compliance audit: < 10s  
✅ API documentation: Auto-generated  

---

## 🐛 Troubleshooting

### **Issue: Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml and restart
```

### **Issue: Database Connection Error**
```bash
# Check PostgreSQL is running
docker compose exec postgres pg_isready

# View database logs
docker compose logs postgres

# Restart database
docker compose restart postgres
```

### **Issue: Services Not Starting**
```bash
# Check Docker is running
docker ps

# View detailed logs
docker compose logs

# Rebuild images
docker compose down
docker compose build --no-cache
docker compose up -d
```

### **Issue: Memory/Resource Problems**
```bash
# Check Docker resource usage
docker stats

# Increase Docker memory limit:
# Docker Desktop → Settings → Resources → Memory (set to 4GB+)

# Or limit services in docker-compose.yml:
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
```

### **Issue: Can't Access http://localhost:8000**
```bash
# Check service is actually running
docker compose ps backend

# Check logs
docker compose logs backend

# Test connection
curl -v http://localhost:8000/health

# If still failing, try:
docker compose restart backend
sleep 5
curl http://localhost:8000/health
```

---

## 📊 Expected Test Results

When you run `test-api.sh`, you should see:

```
===================================
AI Security Platform - API Test
===================================

Test 1: Health Check
Response: {"status":"healthy","app":"AI Security Governance Platform"}
✓ Health check passed

Test 2: Root Endpoint
Response: {"name":"AI Security Governance Platform",...}
✓ Root endpoint working

Test 3: Register AI Model
Response: {"id":1,"name":"test-model-xxxxx","message":"Model registered successfully"}
✓ Model registered with ID: 1

Test 4: Perform Security Risk Assessment
Response: {"id":1,"model_id":1,"overall_risk_score":78.5,"risk_level":"LOW",...}
✓ Risk assessment completed

Test 5: Perform Compliance Audit
Response: {"model_id":1,"overall_compliance_score":85.5,"nist_ai_rmf":{...},...}
✓ Compliance audit completed

...and 5 more tests...

===================================
All Tests Completed Successfully!
===================================
```

---

## 💡 Interview Talking Points

After running this locally, you can say:

> "I built an enterprise AI Security Governance Platform. When you run it locally using Docker, all services start in about 30 seconds. The platform provides 5 key security modules:
> 1. Risk Assessment - evaluates AI model vulnerabilities
> 2. Compliance - audits against NIST AI RMF and EU AI Act
> 3. Data Privacy - detects and protects PII
> 4. Threat Detection - monitors for security anomalies
> 5. Audit Logging - tracks all security activities
>
> The API is fully documented and tested, the infrastructure is defined as code for Azure deployment, and the entire system is optimized for vertical scaling."

---

## 📚 What to Review After Testing

1. **API Documentation**: http://localhost:8000/docs
   - Explore all endpoints
   - Try different request payloads
   - See response structures

2. **Architecture**: Read `docs/ARCHITECTURE.md`
   - Understand the design
   - Learn about security boundaries
   - Review data flow

3. **Scaling**: Read `docs/SCALING.md`
   - Understand vertical scaling approach
   - Learn about resource optimization
   - Review monitoring strategy

4. **Code**: Look at `backend/app/`
   - Review security module structure
   - Understand business logic
   - Check error handling

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Clone & Setup | 2 min |
| Start Services | 3 min |
| Run Tests | 2 min |
| Review Docs | 10 min |
| Explore API | 5 min |
| Review Code | 10 min |
| **Total** | **~32 minutes** |

---

## 🎓 Next Steps

After testing locally:
1. ✅ Understand the architecture
2. ✅ Familiarize with the code
3. ✅ Practice your talking points
4. ✅ Prepare for technical questions
5. ✅ Review the GitHub repository

Good luck with your MTN Group interview! 🚀
