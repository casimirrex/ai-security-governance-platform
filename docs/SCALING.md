# Vertical Scaling Strategy

## Overview

This platform implements **vertical scaling** as its primary scaling strategy, with capabilities to handle growth through increased resource allocation on individual instances rather than adding more instances.

## Vertical Scaling Benefits

### Operational Simplicity
- Fewer servers to manage and monitor
- Simpler deployment pipeline
- Reduced configuration management complexity
- Lower operational overhead

### Cost Efficiency
- Better resource utilization per instance
- Fewer license costs (per-instance services)
- Reduced network overhead
- Lower storage complexity

### Performance
- Lower latency (within-instance communication)
- Reduced network hop counts
- Better CPU cache utilization
- Simpler data consistency management

### Manageability
- Single unified monitoring dashboard
- Simpler debugging and troubleshooting
- Easier to identify bottlenecks
- Simpler security and compliance auditing

## Scaling Tiers

### Tier 1: Development (Small)
```
App Service: Standard B2 (1-2 vCores, 3.5GB RAM)
Database: Standard B_Gen5_1 (1 vCore, 50GB)
Cache: Standard C0 (100MB)
Estimated Users: 10-50
Max Requests/sec: 50
```

### Tier 2: Production Small (Medium)
```
App Service: Standard P1v2 (2 vCores, 3.5GB RAM)
Database: Standard B_Gen5_2 (2 vCores, 100GB)
Cache: Standard C1 (250MB)
Estimated Users: 50-200
Max Requests/sec: 200
```

### Tier 3: Production Medium (Large)
```
App Service: Standard P2v2 (4 vCores, 7GB RAM)
Database: Standard D_Gen5_2 (2 vCores, 200GB)
Cache: Premium P1 (6GB)
Estimated Users: 200-500
Max Requests/sec: 500
```

### Tier 4: Production Large (XL)
```
App Service: Standard P3v2 (8 vCores, 14GB RAM)
Database: Memory Optimized (8 vCores, 500GB)
Cache: Premium P2 (13GB)
Estimated Users: 500-1000
Max Requests/sec: 1000+
```

## Vertical Scaling Implementation

### Application Layer Scaling

**Multi-process Workers**
```python
# Gunicorn configuration for vertical scaling
workers = 4  # Matches CPU cores
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
timeout = 60
```

**Async Request Handling**
```python
# FastAPI with async endpoints
@router.post("/assess")
async def assess_model_security(
    security_data: ModelSecurityData,
    db: Session = Depends(get_db)
):
    # Async operations reduce blocking
    assessment = await service.perform_assessment(db, security_data)
    return assessment
```

**Connection Pooling**
```python
# SQLAlchemy connection pool for vertical scaling
engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

### Database Scaling

**Read Replicas**
```sql
-- Create read replica for query distribution
CREATE REPLICA FROM ai_security_db;
-- Configure application to route read queries to replica
```

**Query Optimization**
```sql
-- Add indexes for frequently accessed columns
CREATE INDEX idx_model_id ON security_risk_assessments(model_id);
CREATE INDEX idx_assessment_date ON security_risk_assessments(assessment_date);
CREATE INDEX idx_model_status ON ai_models(status);

-- Analyze query plans
EXPLAIN ANALYZE
SELECT * FROM security_risk_assessments 
WHERE model_id = 1 AND assessment_date > NOW() - INTERVAL '7 days';
```

**Partitioning Strategy**
```sql
-- Partition large tables for faster queries
CREATE TABLE audit_logs_2024 PARTITION OF audit_logs
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### Cache Layer Optimization

**Redis Configuration**
```yaml
# Docker Compose resource limits
redis:
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 1G
      reservations:
        cpus: '0.5'
        memory: 512M
```

**Cache Warming**
```python
# Preload critical data on application startup
async def init_cache():
    frameworks = await db.query(ComplianceFramework).all()
    for framework in frameworks:
        cache.set(f"framework:{framework.id}", framework)
```

**Cache Invalidation**
```python
# TTL-based invalidation for consistency
@router.post("/assess")
async def assess_model_security(...):
    assessment = await service.perform_assessment(...)
    # Invalidate cache after write
    cache.delete(f"model:{model_id}:assessment")
    return assessment
```

## Monitoring & Auto-Scaling

### Azure Monitor Metrics

```terraform
# Autoscale based on CPU utilization
resource "azurerm_monitor_autoscale_setting" "app_autoscale" {
  profile {
    rule {
      metric_trigger {
        metric_name = "CpuPercentage"
        threshold   = 80
      }
      scale_action {
        type  = "ChangeCount"
        value = 1  # Scale up by 1 instance
      }
    }
  }
}
```

### Key Metrics to Monitor

**Application Metrics**
```yaml
metrics:
  - Request Rate (requests/sec)
  - Response Time (p50, p95, p99)
  - Error Rate (4xx, 5xx)
  - Active Connections
  - CPU Usage
  - Memory Usage
```

**Database Metrics**
```yaml
metrics:
  - Active Connections
  - CPU Percentage
  - Memory Usage
  - Disk I/O
  - Replication Lag
  - Query Performance (slow query log)
```

**Cache Metrics**
```yaml
metrics:
  - Hit Rate
  - Eviction Rate
  - Memory Usage
  - Connected Clients
  - Operations/sec
```

## Scaling Workflow

### Manual Vertical Scaling

1. **Identify Bottleneck**
   ```bash
   # Check current resource usage
   az monitor metrics list --resource /subscriptions/{id}/resourceGroups/{rg}/providers/Microsoft.Web/sites/{app}
   ```

2. **Update Resource Allocation**
   ```bash
   # Scale App Service Plan
   az appservice plan update --sku P2v2 --name {plan} --resource-group {rg}
   ```

3. **Update Database**
   ```bash
   # Scale PostgreSQL
   az postgres flexible-server update --tier MemoryOptimized --sku-name Standard_D4s_v3
   ```

4. **Update Cache**
   ```bash
   # Scale Redis
   az redis update --name {name} --sku Premium --family P --capacity 1
   ```

5. **Monitor & Validate**
   ```bash
   # Check metrics post-scaling
   az monitor metrics list --resource {resource-id} --interval PT1M
   ```

### Automatic Vertical Scaling

```terraform
# Configure autoscaling in Terraform
resource "azurerm_monitor_autoscale_setting" "app_scale" {
  count               = var.enable_autoscaling ? 1 : 0
  target_resource_id  = azurerm_service_plan.ai_security.id
  
  profile {
    capacity {
      default = 2
      minimum = 1
      maximum = 5  # Max vertical scaling instances
    }
    
    rule {
      metric_trigger {
        metric_name = "CpuPercentage"
        threshold   = 80
      }
      scale_action {
        direction = "Increase"
        type      = "PercentChangeCount"
        value     = 50  # Scale up by 50%
      }
    }
  }
}
```

## Load Testing

### K6 Load Test Script

```javascript
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up to 100 users
    { duration: '5m', target: 100 },   // Stay at 100 users
    { duration: '2m', target: 200 },   // Ramp up to 200 users
    { duration: '5m', target: 200 },   // Stay at 200 users
    { duration: '2m', target: 0 },     // Ramp down to 0
  ],
};

export default function() {
  let res = http.post(`${__ENV.BASE_URL}/api/v1/risk-assessment/assess`, {
    model_id: 1,
    has_input_validation: true,
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 5s': (r) => r.timings.duration < 5000,
  });
}
```

## Cost Optimization

### Scaling Cost Comparison

```
Vertical Scaling (Single Large Instance):
- App Service P3v2: ~$300/month
- PostgreSQL 8vCore: ~$2,000/month
- Redis Premium P1: ~$1,100/month
Total: ~$3,400/month (for 500+ concurrent users)

Horizontal Scaling (Multiple Instances):
- 3x App Service P1v2: ~$600/month
- PostgreSQL 2vCore: ~$400/month (plus read replicas: +$400)
- Redis Standard: ~$200/month
Total: ~$1,600/month (for 500+ concurrent users)

Trade-off: Vertical = Simpler, Horizontal = Cheaper at scale
```

## Migration Path

### Phase 1: Small (Months 1-3)
- Single Standard B2 instance
- Standard database (1 vCore)
- Manual monitoring

### Phase 2: Medium (Months 4-8)
- Upgrade to P1v2
- Upgrade database (2 vCores)
- Enable autoscaling
- Add caching layer

### Phase 3: Large (Months 9-12)
- Upgrade to P2v2 or P3v2
- Add read replicas
- Implement advanced caching
- Enhanced monitoring

### Phase 4: Enterprise (Months 12+)
- Memory optimized instances
- Premium cache tier
- Multi-region deployment
- Horizontal scaling if needed

## Troubleshooting

### High CPU Usage
```bash
# Check for CPU-intensive operations
az monitor metrics list --resource {app-id} --metric CpuPercentage
# Scale up instance size
az appservice plan update --sku P2v2
```

### Memory Issues
```bash
# Check memory usage
az monitor metrics list --resource {app-id} --metric MemoryPercentage
# Increase instance size or optimize code
# Review cache settings
```

### Database Slow Queries
```sql
-- Find slow queries
SELECT * FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;

-- Add indexes
CREATE INDEX idx_frequent_query ON table(column);
```

### High Cache Eviction
```bash
# Monitor cache hit rate
# If < 80%, increase cache size
az redis update --name {cache} --sku Premium --family P --capacity 1
```
