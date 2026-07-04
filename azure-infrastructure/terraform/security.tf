# Key Vault for secrets management
resource "azurerm_key_vault" "ai_security" {
  name                        = "ai-sec-kv-${var.environment}-${data.azurerm_client_config.current.account_id}"
  location                    = azurerm_resource_group.ai_security.location
  resource_group_name         = azurerm_resource_group.ai_security.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
  purge_protection_enabled    = true

  tags = {
    Environment = var.environment
  }
}

# Access policy for app service
resource "azurerm_key_vault_access_policy" "app_service" {
  key_vault_id       = azurerm_key_vault.ai_security.id
  tenant_id          = data.azurerm_client_config.current.tenant_id
  object_id          = azurerm_linux_web_app.ai_security_api.identity[0].principal_id
  key_permissions    = []
  secret_permissions = ["Get", "List"]
}

# Network policies
resource "azurerm_key_vault_network_acl" "ai_security" {
  key_vault_id           = azurerm_key_vault.ai_security.id
  default_action         = "Deny"
  bypass                 = "AzureServices"
  virtual_network_subnet_ids = [azurerm_subnet.app_subnet.id]
}

# Managed Identity for App Service
resource "azurerm_user_assigned_identity" "ai_security" {
  name                = "ai-security-identity"
  location            = azurerm_resource_group.ai_security.location
  resource_group_name = azurerm_resource_group.ai_security.name
}

# Data source for current Azure client
data "azurerm_client_config" "current" {}

# Identity for App Service
resource "azurerm_linux_web_app_identity" "ai_security" {
  app_id       = azurerm_linux_web_app.ai_security_api.id
  identity_ids = [azurerm_user_assigned_identity.ai_security.id]
  type         = "SystemAssigned, UserAssigned"

  depends_on = [azurerm_linux_web_app.ai_security_api]
}
