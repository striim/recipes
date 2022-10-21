# Replicating changes and maintaining history in your warehouse with streaming change data capture
## You don’t have to copy data or maintain expensive batch jobs to audit your data

[Link to full recipe](https://www.striim.com/tutorial/https://www.striim.com/tutorial/replicating-changes-and-maintaining-history-in-your-warehouse-with-streaming-change-data-capture/)
![Striim, Retail](https://github.com/striim/recipes/blob/main/CDC-log-history/Image.png)


## Setting Up the Log CDC Application </br>
### Step 1: Set up the source table on Postgres

Create a new table on your source Postgres database with the following query

CREATE TABLE Address( “Serial” integer,
name TEXT,
address TEXT,
PRIMARY KEY (“Serial”));

### Step 2: Set up the target tables on Snowflake

Create an ADDRESS table and HISTORICALADDRESS table on snowflake with the same column names and data types as your source table.

### Step 3: Configure your source and target adapters on Striim

You can download the TQL file from our github repository and deploy it by configuring your source and target as explained in this recipe.

### Step 4: Perform DML operations and stream records to target tables

Deploy and run the Striim app and replicate most updated as well as historical data on your target tables.







