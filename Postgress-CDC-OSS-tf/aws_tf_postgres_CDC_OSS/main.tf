#comment the below code to avoid build config issues in Mac M1 chip
#terraform {
#  required_providers{
#    aws = {
#      source = "hashicorp/aws"
#      version = "~>3.5.0"
#    }
#  }
#}


provider "aws" {
  profile    = "default"
  region     = "us-west-1"
  #enter aws creds if aws cli console is not configured
  #access_key = ""
  #secret_key = ""
}


#sets the budget limits
resource "aws_budgets_budget" "like-and-subscribe" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "20.0"
  limit_unit        = "USD"
  time_unit         = "MONTHLY"
  time_period_start = "2022-07-01_00:01"
}

#creates the VPC 
resource "aws_vpc" "test" {
  cidr_block = "10.0.0.0/16"
}

#configured to test vpc 
data "aws_vpc" "test" {
  default = true
}

#security group
resource "aws_security_group" "test-security-group" {
  vpc_id      = data.aws_vpc.test.id
  name        = "aws-sec-group"
  description = "Allow all inbound for Postgres"
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

/*********************
Postgres related 
**********************/


#db password constraints
resource "random_string" "postgres-db-password" {
  length  = 22
  upper   = true
  numeric = true
  special = false
}

#sets the logical replication and public access
resource "aws_db_parameter_group" "postgres" {
  name        = "postgres-cdc-logical-decoding"
  family      = "postgres13"
  description = "RDS server - Postgres parameter group enabling logical decoding"

  parameter {
    name         = "rds.logical_replication"
    value        = 1
    apply_method = "pending-reboot"
  }
}

resource "aws_db_instance" "aws-pg-cdc" {
  identifier             = "aws-pg-cdc"
  db_name                = "tfawspgsource"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "13.4"
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.test-security-group.id]
  username               = "mike"
  password               = "random_string.postgres-db-password.result}"
}