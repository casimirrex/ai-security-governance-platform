# Virtual Network
resource "azurerm_virtual_network" "ai_security" {
  name                = "ai-security-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.ai_security.location
  resource_group_name = azurerm_resource_group.ai_security.name
}

# Subnet for application
resource "azurerm_subnet" "app_subnet" {
  name                 = "app-subnet"
  resource_group_name  = azurerm_resource_group.ai_security.name
  virtual_network_name = azurerm_virtual_network.ai_security.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Subnet for database
resource "azurerm_subnet" "db_subnet" {
  name                 = "db-subnet"
  resource_group_name  = azurerm_resource_group.ai_security.name
  virtual_network_name = azurerm_virtual_network.ai_security.name
  address_prefixes     = ["10.0.2.0/24"]
}

# Network Security Group for App
resource "azurerm_network_security_group" "app_nsg" {
  name                = "app-nsg"
  location            = azurerm_resource_group.ai_security.location
  resource_group_name = azurerm_resource_group.ai_security.name

  security_rule {
    name                       = "AllowHTTP"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "AllowHTTPS"
    priority                   = 101
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# Network Security Group for Database
resource "azurerm_network_security_group" "db_nsg" {
  name                = "db-nsg"
  location            = azurerm_resource_group.ai_security.location
  resource_group_name = azurerm_resource_group.ai_security.name

  security_rule {
    name                       = "AllowPostgres"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5432"
    source_address_prefix      = "10.0.1.0/24"
    destination_address_prefix = "*"
  }
}
