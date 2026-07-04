# Azure Database for PostgreSQL - Flexible Server
resource "azurerm_postgresql_flexible_server" "ai_security" {
  name                   = "ai-security-db-${var.environment}"
  location               = azurerm_resource_group.ai_security.location
  resource_group_name    = azurerm_resource_group.ai_security.name
  administrator_login    = "psqladmin"
  administrator_password = random_password.db_password.result
  sku_name               = var.database_sku
  storage_mb             = 32768
  version                = "15"

  zone = "1"

  backup_retention_days        = 30
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  tags = {
    Environment = var.environment
  }
}

# Database
resource "azurerm_postgresql_flexible_server_database" "ai_security" {
  name            = "ai_security_db"
  server_id       = azurerm_postgresql_flexible_server.ai_security.id
  charset         = "UTF8"
  collation       = "en_US.utf8"
}

# Firewall rule for app subnet
resource "azurerm_postgresql_flexible_server_firewall_rule" "app" {
  name             = "allow-app"
  server_id        = azurerm_postgresql_flexible_server.ai_security.id
  start_ip_address = "10.0.1.0"
  end_ip_address   = "10.0.1.255"
}

# Random password for database
resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Store database password in Key Vault
resource "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  value        = random_password.db_password.result
  key_vault_id = azurerm_key_vault.ai_security.id
}

# Cache for vertical scaling
resource "azurerm_redis_cache" "ai_security" {
  name                = "ai-security-cache-${var.environment}"
  location            = azurerm_resource_group.ai_security.location
  resource_group_name = azurerm_resource_group.ai_security.name
  capacity            = 2
  family              = "C"
  sku_name            = "Standard"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"

  tags = {
    Environment = var.environment
  }
}
