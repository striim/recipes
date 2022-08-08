variable "project" {
  description = "The project to deploy to, if not set the default provider project is used."
  default     = "gcpstriimproj"
}

variable "region" {
  description = "Region for cloud resources"
  default     = "us-south1"
}

variable "database_version" {
  description = "The version of of the database. For example, `MYSQL_5_6` or `POSTGRES_9_6`."
  default     = "POSTGRES_13"
}

variable "database_name" {
  description = "the name of the database created inside the postgres instance"
  default = "mydatabase"
}

variable "tier" {
  description = "Refer to https://cloud.google.com/sql/pricing supported tiers and pricing"
  default     = "db-custom-1-3840" //"db-f1-micro"
}

variable "activation_policy" {
  description = "Acceptable values are as follows: `ALWAYS`, `NEVER` or `ON_DEMAND`."
  default     = "ALWAYS"
}

variable "disk_autoresize" {
  description = "Configuration to increase storage size automatically in Second generation only"
  default     = false
}

variable "disk_size" {
  description = "The size of data disk, in GB. Size of a running instance cannot be reduced but can be increased. NOTE: Second generation only."
  default     = 10
}

variable "disk_type" {
  description = "Second generation only. The type of data disk can be: `PD_SSD` or `PD_HDD`."
  default     = "PD_HDD"
}

variable "availability_type" {
  description = "Specifies set up for high availability (REGIONAL) or single zone (ZONAL)."
  default     = "ZONAL"
}

variable "db_instance_access_cidr" {
  description = "The IPv4 CIDR to provide access the database instance - replace the below value with private ip for additional security"
  default = "0.0.0.0/0"
}

variable "instance_deletion_protection"{
    description = "Provides necessary permission for Terraform destroy to perform cleanup"
    default = false
}



