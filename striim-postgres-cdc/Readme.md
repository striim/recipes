# Stream CDC Data from PostgreSQL to Google BigQuery with Striim Cloud 
## Use Striim Cloud to stream CDC data securely from PostgreSQL database into Google BigQuery

[Link to full recipe](https://www.striim.com/tutorial/stream-data-from-postgresql-to-google-bigquery-with-striim-cloud-part-2/)

![Striim, PostgresCDC](https://github.com/striim/recipes/blob/main/striim-postgres-cdc/image.png)

## Setting Up the Postgres to BigQuery Streaming Application </br>

### Step 1: Follow this [recipe](https://www.striim.com/tutorial/stream-data-from-postgresql-to-google-bigquery-with-striim-cloud-part-2/) to create a Replication Slot and user for Change Data Capture

The replication user reads change data from your source database and replicates it to the target in real-time.

### Step 2: Download the dataset and TQL file from our github repo and set up your Postgres Source and BigQuery Target.

You can find the csv dataset in our github repo. Set up your BigQuery dataset and table that will act as a target for the streaming application

### Step 3: Configure source and target components in the  app

Configure the source and target components in the striim app. Please follow the detailed steps from our [recipe](https://www.striim.com/tutorial/stream-data-from-postgresql-to-google-bigquery-with-striim-cloud-part-2/).

### Step 4: Run the streaming app 

Deploy and run real-time data streaming app 
