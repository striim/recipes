# Instance Builds 

### This `instance-builds` directory stores the Terraform to deploy and define Striim server in AWS and the infrastructure to turn on/off EC2 and RDS instances.

Deploys the following resources:

  1) S3 bucket to store Terraform's state file (Encrypted) and Dynamodb table to store Terraform lock id.
  2) Security group with Striim open port 9080 (Striim's designated port).
  3) EC2 instance with the attached security group and latest Striim image.
  4) Instance scheduler infrastructure:
     - 2 Lambdas (One to stop RDS/EC2 instances and the other one to start the instances)
     - 2 Eventbridge rules (Starts the EC2 and RDS instances at 8:00AM PST and turns it off at 8:00PM PST)
     - IAM roles with permission to invoke lambdas, describe EC2/RDS instances, start/stop instances and etc...
     



