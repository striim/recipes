# Image Builds 

### This `image-builds` directory stores an Ansible playbook that creates a Striim image for CentOS and uses Packer tool to deploy the image to AWS, Azure and Google Cloud Platform.

Ansible Playbook:

  1) Installs Java (JDK 1.8) and sets it to the path.
  2) Installs Striim with credentials.
  3) Installs postgresql server and libraries.
  4) Builds a postgres source and target databases with schemas and tables for testing purposes. (Only on AWS AMI)


