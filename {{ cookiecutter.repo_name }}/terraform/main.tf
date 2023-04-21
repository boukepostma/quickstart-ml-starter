terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">=3.17.0"
    }
  }  
}

provider "azurerm" {
  features{}
  subscription_id   = var.arm_subscription_id
  tenant_id         = var.arm_tenant_id
  client_id         = var.arm_client_id
  client_secret     = var.arm_client_secret
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "default" {
  name     = "${var.prefix}-${var.environment}-rg"
  location = var.location
}
