# App Service Plan for vertical scaling
resource "azurerm_service_plan" "ai_security" {
  name                = "ai-security-asp"
  location            = azurerm_resource_group.ai_security.location
  resource_group_name = azurerm_resource_group.ai_security.name
  os_type             = "Linux"
  sku_name            = var.app_service_plan_sku

  tags = {
    Environment = var.environment
  }
}

# App Service for Backend API
resource "azurerm_linux_web_app" "ai_security_api" {
  name                = "ai-security-api-${var.environment}"
  location            = azurerm_resource_group.ai_security.location
  resource_group_name = azurerm_resource_group.ai_security.name
  service_plan_id     = azurerm_service_plan.ai_security.id

  site_config {
    application_stack {
      docker_image_name   = "ai-security-governance:latest"
      docker_registry_url = "https://ghcr.io"
    }

    always_on                = true
    minimum_tls_version      = "1.2"
    scm_minimum_tls_version  = "1.2"
    http2_enabled            = true
    websockets_enabled       = true
    managed_pipeline_mode    = "Integrated"
    load_balancing_mode      = "LeastRequests"
  }

  app_settings = {
    "ENVIRONMENT"              = var.environment
    "DOCKER_REGISTRY_SERVER_URL" = "https://ghcr.io"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
  }

  tags = {
    Environment = var.environment
  }
}

# App Service Autoscale Settings
resource "azurerm_monitor_autoscale_setting" "app_autoscale" {
  count               = var.enable_autoscaling ? 1 : 0
  name                = "app-autoscale"
  resource_group_name = azurerm_resource_group.ai_security.name
  location            = azurerm_resource_group.ai_security.location
  target_resource_id  = azurerm_service_plan.ai_security.id

  profile {
    name = "vertical-scaling-profile"

    capacity {
      default = 2
      minimum = 1
      maximum = 5
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_service_plan.ai_security.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        operator           = "GreaterThan"
        threshold          = 80
      }

      scale_action {
        direction = "Increase"
        type      = "PercentChangeCount"
        value     = "50"
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_service_plan.ai_security.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        operator           = "LessThan"
        threshold          = 30
      }

      scale_action {
        direction = "Decrease"
        type      = "PercentChangeCount"
        value     = "25"
        cooldown  = "PT5M"
      }
    }
  }
}
