output "app_service_url" {
  description = "URL of the App Service"
  value       = "https://${azurerm_linux_web_app.ai_security_api.default_hostname}"
}

output "api_endpoint" {
  description = "API endpoint"
  value       = "https://${azurerm_linux_web_app.ai_security_api.default_hostname}/api/v1"
}

output "database_connection_string" {
  description = "PostgreSQL connection string (sensitive)"
  value       = "postgresql://psqladmin:${random_password.db_password.result}@${azurerm_postgresql_flexible_server.ai_security.fqdn}:5432/ai_security_db"
  sensitive   = true
}

output "database_host" {
  description = "PostgreSQL database host"
  value       = azurerm_postgresql_flexible_server.ai_security.fqdn
}

output "redis_endpoint" {
  description = "Redis cache endpoint"
  value       = "${azurerm_redis_cache.ai_security.hostname}:${azurerm_redis_cache.ai_security.port}"
}

output "keyvault_url" {
  description = "Key Vault URL"
  value       = azurerm_key_vault.ai_security.vault_uri
}

output "app_insights_instrumentation_key" {
  description = "Application Insights instrumentation key"
  value       = azurerm_application_insights.ai_security.instrumentation_key
  sensitive   = true
}

output "log_analytics_workspace_id" {
  description = "Log Analytics Workspace ID"
  value       = azurerm_log_analytics_workspace.ai_security.id
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.ai_security.name
}
