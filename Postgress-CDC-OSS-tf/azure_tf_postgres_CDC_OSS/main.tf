#provides configuration details for terraform
#keep below code block commented to run in Mac M1 
/*
terraform {
    required_providers {
      azurerm = {
        source = "hashicorp/azurerm"
        version = "~>2.31.1"
      }
    }
}
*/

provider "azurerm" {
    features {
      /* removing features block will lead to build issues, 
      leave empty if no features are required */
    }
  
}

#Resource group 
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "West Europe"
}

#Whitelisting ip/Security:
#Change the start_ip_address and end_ip_address for more security - currently set to public
# https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/postgresql_firewall_rule
resource "azurerm_postgresql_firewall_rule" "name" {
  name                = "AllowAll"
  resource_group_name = azurerm_resource_group.example.name
  server_name         = azurerm_postgresql_server.example.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
  
}


############ POSTGRES INITIALIZING ##############

resource "azurerm_postgresql_server" "example" {
  name                = "tf-psqlserver"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  administrator_login          = "psqladmin"
  administrator_login_password = "Formula1"
  
  sku_name   = "B_Gen5_1"   #"tier"_"family"_"core"
  version    = "11"
  storage_mb = 5120

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = false


  public_network_access_enabled    = true
  ssl_enforcement_enabled          = false
  ssl_minimal_tls_version_enforced = "TLSEnforcementDisabled"

  #running Azure CLI commands to enable replication - logical decoding for CDC
  provisioner "local-exec" {
    command = "az postgres server configuration set --resource-group example-resources --server-name tf-psqlserver --name azure.replication_support --value logical"
    on_failure = fail
  }
  #Server needs to restart after logical decoding has been set
  provisioner "local-exec" {
    command = "az postgres server restart --resource-group example-resources --name tf-psqlserver"
  }
}