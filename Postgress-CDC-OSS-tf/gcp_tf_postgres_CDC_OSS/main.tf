//setup the GCP provider 
//keep commented for Mac M1 chip
/*
terraform {
  required_version = ">= 0.12"
}
*/


terraform {
  required_providers {
    postgresql = {
      source = "cyrilgdn/postgresql"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.region
}

provider "postgresql" {
  scheme   = "gcppostgres"
  host     = google_sql_database_instance.postgres.connection_name
  username = google_sql_user.users.name
  password = google_sql_user.users.password
  superuser = true
}


//Enable the API for the services 
resource "google_project_service" "service" {
  for_each = toset([
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com"
  ])
  service = each.key
  project            = var.project
  disable_on_destroy = false
}


resource "random_string" "postgres-db-name" {
  length  = 4
  upper   = false
  numeric = false
  special = false
}

//POSTGRES CONFIG:
resource "google_sql_database_instance" "postgres" {
  name = "tf-postgres-instance-${random_string.postgres-db-name.result}"
  database_version = var.database_version
  deletion_protection = var.instance_deletion_protection
  settings{
    tier = var.tier
    activation_policy = var.activation_policy
    disk_autoresize = var.disk_autoresize
    disk_size = var.disk_size
    disk_type = var.disk_type
    availability_type = var.availability_type
    
    ip_configuration {
      ipv4_enabled = "true"
      authorized_networks {
        value = "${var.db_instance_access_cidr}"
      }
    }
    backup_configuration {
      binary_log_enabled = false
      enabled = false
    }
    database_flags {
      name  = "cloudsql.logical_decoding" 
      value = "on"
    }
  }
}


resource "google_sql_user" "users" {
  name     = "janedoe"
  instance = google_sql_database_instance.postgres.name
  password = "postgres"
  deletion_policy = "ABANDON"
}


resource "google_sql_database" "database" {
  name     = var.database_name
  instance = google_sql_database_instance.postgres.name
}