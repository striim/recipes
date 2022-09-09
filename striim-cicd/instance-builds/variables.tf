variable "aws_access_key" {
  type        = string
  description = "AWS access key"
}

variable "aws_secret_key" {
  type        = string
  description = "AWS secret key"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
}

variable "vm_instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "m5.4xlarge"
}

variable "vm_associate_public_ip_address" {
  type        = bool
  description = "Associate a public IP address to the EC2 instance"
  default     = true
}

variable "vm_root_volume_size" {
  type        = number
  default     = 50
  description = "Root Volume size of the EC2 Instance"
}

variable "vm_data_volume_size" {
  type        = number
  default     = 20
  description = "Data volume size of the EC2 Instance"
}

variable "vm_root_volume_type" {
  type        = string
  description = "Root volume type of the EC2 Instance"
  default     = "gp2"
}

variable "vm_data_volume_type" {
  type        = string
  description = "Data volume type of the EC2 Instance"
  default     = "gp2"
}

variable "subnet_id" {
  type        = string
  description = "Subnet Id"
  default     = "subnet-d1806f89"
}

variable "vpc_id" {
  type        = string
  description = "VPC Id"
  default     = "vpc-104df574"
}
variable "key_name" {
  type        = string
  description = "Key name"
  default     = "striim_key"
}
