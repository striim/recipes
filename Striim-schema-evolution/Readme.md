# Capture Schema Evolution from Postgres CDC source and Stream changes to Snowflake with Striim
## Use Striim to handle schema changes on source database in real-time
	

[Link to full recipe](https://www.striim.com/tutorial/capture-schema-evolution-from-postgres-cdc-source-and-stream-changes-to-snowflake/)
![Striim, schema evolution](https://github.com/striim/recipes/blob/main/Striim-schema-evolution/schemaevol.png)

## Setting Up Striim app to capture Schema Evolution </br>

### Step 1: Create Replication Slot and Replication User on Postgres

Follow this [recipe](https://www.striim.com/tutorial/stream-data-from-postgresql-to-google-bigquery-with-striim-cloud-part-2/) to create a Replication Slot and user for Change Data Capture. The replication user reads change data from your source database and replicates it to the target in real-time.

### Step 2: Setup CDDL Capture Procedure and CDDL Tracking Table
 
Follow the [recipe](https://www.striim.com/tutorial/capture-schema-evolution-from-postgres-cdc-source-and-stream-changes-to-snowflake/) to configure PostgreSQL CDDL Capture Procedure and CDDL Tracking Table. You can find the sql queries in our github repository 

### Step 3: Create CDC app on Striim server

Create the CDC app that handles Schema Evolution on Striim SaaS as shown in the recipe

### Step 4: Deploy and Run the Striim app

Run the App and check the message logs and target table for any DDL changes.
