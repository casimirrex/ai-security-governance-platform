variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "ai-security-governance-rg"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}

variable "app_service_plan_sku" {
  description = "App Service Plan SKU for vertical scaling"
  type        = string
  default     = "P1v2"
}

variable "database_sku" {
  description = "PostgreSQL database SKU for vertical scaling"
  type        = string
  default     = "B_Gen5_2"
}

variable "vm_size" {
  description = "Virtual machine size for vertical scaling"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "enable_autoscaling" {
  description = "Enable autoscaling for resources"
  type        = bool
  default     = true
}
