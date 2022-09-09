# Striim CI/CD Repository - Business Development
### The purpose of this CI/CD pipeline is to deploy PoC infrastructure/resources to all cloud providers (AWS, Azure, and Google Cloud).

1) Deploys Striim images to all cloud providers.
    - Java JDK (1.8)
    - Striim (4.1.0)
    - PostgreSQL server
    - PostgreSQL source and target databases, users, tables and dummy data
2) Deploys Striim server to AWS as an EC2 instance with the latest image attached.
3) Deploys instance scheduler infrastructure to AWS.
4) Defines the CI/CD pipeline using Github Actions tools.

### How to use this pipeline:
1) To deploy a new Striim image version to all cloud providers:
    - Click on 'Actions' tab.
    - Select 'Image builds pipeline' on the left panel.
    - Click on 'Run Workflow' dropdown, select 'main' branch to get the latest changes and then click on 'Run workflow' button.
 
2) To deploy/update a Striim EC2 instance with the latest image:
    - Click on 'Actions' tab.
    - Select 'Instance builds pipeline' on the left panel.
    - Click on 'Run Workflow' dropdown, select 'main' branch to get the latest changes and then click on 'Run workflow' button.
    
### How to start Striim server and accessing PostgreSQL database:
1) To access and run the Striim server:
     - Login to your AWS console and go to EC2 console.
     - Ask your admin to provide you the striim_key.pem key.
     - Search for an instance named 'striim-server'.
     - Grab the ssh command after the 'Connect' button. (i.e. `ssh -i "<path>/<to>/<key>/striim_key.pem" ec2-user@ec2-54-213-129-76.us-west-2.compute.amazonaws.com`.
     - Execute the command in your terminal and access your striim instance.
     - Once inside of your instance, go to `/op/Striim/bin/` directory.
     - Run `sudo ./server.sh` and wait until it's succesfully done.
     - Grab your intance public IP and type in the following in your web browser: `<public IP>:9080`

2) To access the PostgreSQL database in the EC2 instance, run the following command:
    - `psql -h localhost -U postgres -d source_db`
    - To access/view Postgres schema, table or data, run the following:
        - `set search_path to source_schema;` -> Sets the schema.
        - `\dt` -> View all tables.
        - `SELECT COUNT(*) FROM employee` -> Make sure there's ~1.5 Million records in the table.
 
      
