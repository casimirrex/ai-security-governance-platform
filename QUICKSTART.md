# Quick Start Guide - AI Security Governance Platform

**⏱️ Time Required: 5 minutes to run**

## Prerequisites

Make sure you have:
- ✅ Docker & Docker Compose
- ✅ Git
- ✅ ~2GB free disk space

## Run in 3 Commands

```bash
# 1. Clone the repository
git clone https://github.com/casimirrex/ai-security-governance-platform.git
cd ai-security-governance-platform

# 2. Copy environment file
cp .env.example .env

# 3. Start all services (PostgreSQL, Redis, FastAPI, Prometheus, Grafana)
docker compose up -d
```

## Verify Services

```bash
# Wait 10 seconds for all services to start
sleep 10

# Check all services are running
docker compose ps

# Expected: 5 containers running (backend, postgres, redis, prometheus, grafana)
```

## Test the Application

```bash
# 1. Health Check
curl http://localhost:8000/health

# 2. View API Documentation (Interactive)
open http://localhost:8000/docs

# 3. Run Automated Tests
bash test-api.sh
```

## Access Services

| Service | URL | Purpose |
|---------|-----|---------|
| **API Docs** | http://localhost:8000/docs | Interactive API testing |
| **Prometheus** | http://localhost:9090 | Metrics collection |
| **Grafana** | http://localhost:3001 | Dashboards (admin/admin) |

## Common Commands

```bash
# View live logs
docker compose logs -f backend

# Stop all services
docker compose down

# Clean everything (including data)
docker compose down -v

# Restart a service
docker compose restart backend
```

## Next Steps

1. **Understand Architecture**: Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. **Vertical Scaling**: Read [docs/SCALING.md](docs/SCALING.md)
3. **Complete Setup Guide**: Read [LOCAL_TESTING.md](LOCAL_TESTING.md)
4. **Deploy to Azure**: Read [docs/SETUP.md](docs/SETUP.md#azure-deployment)

## Troubleshooting

### Services not starting?
```bash
docker compose down -v
docker compose up -d
sleep 15
```

### Port already in use?
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Database connection error?
```bash
# Restart database
docker compose restart postgres
sleep 5
curl http://localhost:8000/health
```

## What You'll See

When you run the tests, you'll see:

✓ Health check passes  
✓ Models can be registered  
✓ Risk assessments complete  
✓ Compliance audits run  
✓ Data privacy checks execute  
✓ Threat detection works  
✓ Audit logs are created  

All in **< 10 seconds total**.

## Architecture Overview

```
┌──────────────────────────────────┐
│   FastAPI Backend (Port 8000)    │
├──────────────────────────────────┤
│  ✓ Risk Assessment Service       │
│  ✓ Compliance Service            │
│  ✓ Data Privacy Service          │
│  ✓ Threat Detection Service      │
│  ✓ Audit Logging Service         │
└────────────────┬─────────────────┘
                 │
    ┌────────────┴───────────┐
    │                        │
PostgreSQL Database      Redis Cache
  (Port 5432)          (Port 6379)
```

## Interview Talking Points

> "I've built an enterprise AI Security Governance Platform with 5 vertically-organized security modules. When you run it with Docker, all services start in seconds. The platform provides risk assessment for AI models, compliance automation against NIST AI RMF and EU AI Act, PII detection in data, real-time threat monitoring, and complete audit trails. It's designed with vertical scaling in mind and integrates with Azure security services."

---

**Ready? Run `docker compose up -d` now!** 🚀
