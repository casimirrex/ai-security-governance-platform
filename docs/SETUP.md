# Setup Guide

## Project Structure

```
ai-security-governance-platform/
├── README.md                          # Project overview
├── .env.example                        # Environment variables template
├── docker-compose.yml                  # Local development setup
├── .github/
│   └── workflows/                      # CI/CD pipelines
│       ├── ci.yml                      # Build and test pipeline
│       └── security-scan.yml           # Security scanning pipeline
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application entry point
│   │   ├── config.py                   # Configuration management
│   │   ├── database.py                 # Database setup
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/          # API endpoints
│   │   └── security_modules/           # Vertically organized security modules
│   │       ├── risk_assessment/
│   │       ├── compliance/
│   │       ├── data_privacy/
│   │       ├── threat_detection/
│   │       └── audit_logging/
│   ├── requirements.txt                # Python dependencies
│   ├── Dockerfile                      # Container image definition
│   └── tests/                          # Test suite
├── azure-infrastructure/
│   └── terraform/                      # Infrastructure as Code
│       ├── main.tf
│       ├── variables.tf
│       ├── networking.tf
│       ├── compute.tf
│       ├── database.tf
│       ├── security.tf
│       ├── monitoring.tf
│       └── outputs.tf
├── docs/
│   ├── ARCHITECTURE.md                 # System design documentation
│   ├── SCALING.md                      # Vertical scaling strategy
│   ├── API.md                          # API documentation
│   └── DEPLOYMENT.md                   # Deployment guide
└── monitoring/
    └── prometheus.yml                  # Prometheus configuration
```

## Prerequisites

### Local Development
- Python 3.11+
- Docker & Docker Compose
- Git
- PostgreSQL client tools (optional)

### Cloud Deployment (Azure)
- Azure CLI
- Terraform 1.0+
- Azure subscription
- Service Principal credentials

## Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-security-governance-platform.git
cd ai-security-governance-platform
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

### 3. Start Services with Docker Compose
```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps

# Check service logs
docker-compose logs -f backend
```

### 4. Initialize Database
```bash
# Access the backend container
docker-compose exec backend bash

# Run database migrations
alembic upgrade head

# Create initial admin user
python -m scripts.create_admin
```

### 5. Test the API
```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs

# Register a model
curl -X POST http://localhost:8000/api/v1/risk-assessment/register-model \
  -H "Content-Type: application/json" \
  -d '{
    "name": "model1",
    "description": "Test model",
    "model_type": "neural_network",
    "framework": "tensorflow",
    "version": "1.0.0"
  }'
```

## Backend Development

### Setting up Python Environment (Without Docker)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v --cov=app

# Code formatting
black app

# Linting
flake8 app

# Type checking
mypy app
```

### Project Structure Details

```
backend/app/
├── main.py                    # FastAPI application
├── config.py                  # Settings and configuration
├── database.py                # Database connection and ORM setup
├── api/
│   └── v1/
│       ├── __init__.py        # Router aggregation
│       └── endpoints/
│           ├── risk_assessment.py    # Risk assessment endpoints
│           ├── compliance.py         # Compliance audit endpoints
│           ├── data_privacy.py       # Data privacy endpoints
│           ├── threat_detection.py   # Threat detection endpoints
│           └── audit_logging.py      # Audit logging endpoints
└── security_modules/          # Core security logic (vertically organized)
    ├── risk_assessment/
    │   ├── models.py          # SQLAlchemy ORM models
    │   ├── service.py         # Business logic
    │   └── __init__.py
    ├── compliance/
    ├── data_privacy/
    ├── threat_detection/
    └── audit_logging/
```

### Adding New Endpoints

1. Create a new endpoint file in `app/api/v1/endpoints/`:
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_status():
    return {"status": "ok"}
```

2. Include in `app/api/v1/__init__.py`:
```python
from .endpoints import new_endpoint
api_router.include_router(
    new_endpoint.router,
    prefix="/new",
    tags=["New Feature"]
)
```

## Azure Deployment

### 1. Prerequisites
```bash
# Install Azure CLI
brew install azure-cli  # macOS
# or download from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login to Azure
az login

# Set subscription
az account set --subscription "Your Subscription ID"
```

### 2. Create Service Principal for Terraform
```bash
# Create service principal
az ad sp create-for-rbac --name ai-security-sp --role Contributor

# Note the: appId, password, and tenantId
```

### 3. Terraform Setup
```bash
cd azure-infrastructure/terraform

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
resource_group_name = "ai-security-governance-rg"
location = "eastus"
environment = "production"
app_service_plan_sku = "P1v2"
database_sku = "Standard_B_Gen5_2"
EOF

# Initialize Terraform
terraform init

# Review changes
terraform plan

# Apply infrastructure
terraform apply
```

### 4. Container Registry Setup
```bash
# Create container registry
az acr create --resource-group ai-security-governance-rg \
  --name aisecurityregistry \
  --sku Standard

# Login to registry
az acr login --name aisecurityregistry

# Build and push image
docker build -t aisecurityregistry.azurecr.io/ai-security:latest ./backend
docker push aisecurityregistry.azurecr.io/ai-security:latest
```

### 5. Deploy to App Service
```bash
# Configure app service with container
az appservice plan create \
  --name ai-security-asp \
  --resource-group ai-security-governance-rg \
  --sku P1V2 --is-linux

az webapp create \
  --resource-group ai-security-governance-rg \
  --plan ai-security-asp \
  --name ai-security-api-prod \
  --deployment-container-image-name aisecurityregistry.azurecr.io/ai-security:latest
```

### 6. Configure Environment Variables
```bash
# Set environment variables
az webapp config appsettings set \
  --resource-group ai-security-governance-rg \
  --name ai-security-api-prod \
  --settings \
  ENVIRONMENT=production \
  DATABASE_URL="$(terraform output -raw database_connection_string)" \
  REDIS_URL="$(terraform output -raw redis_endpoint)" \
  AZURE_KEYVAULT_URL="$(terraform output -raw keyvault_url)"
```

## Testing

### Unit Tests
```bash
# Run all tests
pytest tests/unit -v

# Run specific test
pytest tests/unit/test_risk_assessment.py -v

# Run with coverage
pytest tests/unit --cov=app --cov-report=html
```

### Integration Tests
```bash
# Run integration tests (requires running services)
pytest tests/integration -v
```

### Load Testing
```bash
# Install k6
brew install k6

# Run load test
k6 run monitoring/load-test.js
```

## Monitoring & Troubleshooting

### View Logs
```bash
# Backend logs
docker-compose logs -f backend

# Database logs
docker-compose logs -f postgres

# Cache logs
docker-compose logs -f redis
```

### Database Access
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d ai_security_db

# Useful queries
SELECT * FROM ai_models;
SELECT * FROM security_risk_assessments;
SELECT * FROM audit_logs;
```

### Performance Monitoring
```bash
# Prometheus metrics
open http://localhost:9090

# Grafana dashboards
open http://localhost:3001

# Default credentials: admin/admin
```

## Common Issues & Solutions

### Issue: Port Already in Use
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Issue: Database Connection Error
```bash
# Verify PostgreSQL is running
docker-compose exec postgres pg_isready

# Check connection string in .env
DATABASE_URL=postgresql://postgres:password@postgres:5432/ai_security_db
```

### Issue: Redis Connection Failed
```bash
# Restart Redis
docker-compose restart redis

# Check Redis connectivity
docker-compose exec redis redis-cli ping
```

### Issue: Out of Memory
```bash
# Increase Docker memory allocation
# In Docker Desktop: Settings → Resources → Memory

# Or update docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
```

## Next Steps

1. **Review Architecture**: Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Understand Scaling**: Review [SCALING.md](SCALING.md)
3. **API Integration**: Check [API.md](API.md) for endpoint details
4. **Deployment**: Follow [DEPLOYMENT.md](DEPLOYMENT.md) for production

## Support

For issues and questions:
1. Check existing GitHub issues
2. Create a new GitHub issue with:
   - Error message/logs
   - Steps to reproduce
   - Environment details (OS, Docker version, etc.)

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes with tests
3. Run linting and tests: `make test lint`
4. Commit with meaningful messages
5. Push and create a Pull Request

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Azure Documentation](https://docs.microsoft.com/en-us/azure/)
- [Terraform Documentation](https://www.terraform.io/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
