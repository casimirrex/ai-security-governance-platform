# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "ai_security" {
  name                = "ai-security-law-${var.environment}"
  location            = azurerm_resource_group.ai_security.location
  resource_group_name = azurerm_resource_group.ai_security.name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = {
    Environment = var.environment
  }
}

# Application Insights
resource "azurerm_application_insights" "ai_security" {
  name                = "ai-security-ai-${var.environment}"
  location            = azurerm_resource_group.ai_security.location
  resource_group_name = azurerm_resource_group.ai_security.name
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.ai_security.id

  tags = {
    Environment = var.environment
  }
}

# Diagnostic settings for App Service
resource "azurerm_monitor_diagnostic_setting" "app_service" {
  name               = "app-service-diagnostics"
  target_resource_id = azurerm_linux_web_app.ai_security_api.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.ai_security.id

  log {
    category = "AppServiceHTTPLogs"
    enabled  = true
  }

  log {
    category = "AppServiceConsoleLogs"
    enabled  = true
  }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}

# Diagnostic settings for PostgreSQL
resource "azurerm_monitor_diagnostic_setting" "database" {
  name               = "database-diagnostics"
  target_resource_id = azurerm_postgresql_flexible_server.ai_security.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.ai_security.id

  log {
    category = "PostgreSQLLogs"
    enabled  = true
  }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}

# Action Group for alerts
resource "azurerm_monitor_action_group" "ai_security" {
  name                = "ai-security-alerts"
  resource_group_name = azurerm_resource_group.ai_security.name
  short_name          = "aisg"

  email_receiver {
    name          = "admin"
    email_address = "admin@example.com"
  }
}

# Alert for high CPU
resource "azurerm_monitor_metric_alert" "cpu_high" {
  name                = "cpu-high"
  resource_group_name = azurerm_resource_group.ai_security.name
  scopes              = [azurerm_service_plan.ai_security.id]
  description         = "Alert when CPU usage is high"

  criteria {
    metric_name      = "CpuPercentage"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 85
    metric_namespace = "Microsoft.Web/serverfarms"
  }

  action {
    action_group_id = azurerm_monitor_action_group.ai_security.id
  }
}

# Alert for database connections
resource "azurerm_monitor_metric_alert" "db_connections_high" {
  name                = "db-connections-high"
  resource_group_name = azurerm_resource_group.ai_security.name
  scopes              = [azurerm_postgresql_flexible_server.ai_security.id]
  description         = "Alert when database connections are high"

  criteria {
    metric_name      = "active_connections"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 80
    metric_namespace = "Microsoft.DBforPostgreSQL/flexibleServers"
  }

  action {
    action_group_id = azurerm_monitor_action_group.ai_security.id
  }
}
