# Ensure Data Freshness with Streaming SQL
## Use Striim’s SQL to monitor and alert on lag between source and target systems
        

[Link to full recipe](https://www.striim.com/tutorial/ensure-data-freshness-with-streaming-sql/)
![Striim, schema evolution](https://github.com/striim/recipes/blob/main/striim-Lag-monitor/Image.png)


## Setting Up the Utility </br>

### Step 1: Download the TQL files

You can download the TQL files for streaming app and lag monitor app from our github repository. Deploy the lag monitor app on your Striim server.

### Step 2: Set up the source and Target for streaming app

You can use any Striim app of your choice and monitor the data freshness. Please checkout our tutorials and recipes to  learn how to set up streaming applications with various sources and targets.

### Step 3: Edit the csv file

The first column of  lagthreshold csv file lists the names of target tables that are monitored and second column contains the SLA in minutes. The third column is optional and is used in case of email alerts. Upload the csv file and enter the filepath in the FileReader component of your app as explained in ‘Lag Threshold CSV and Continuous Query’ section of this recipe

### Step 4: Upload the .scm file

If you do not have Global.admin permission, please reach out to cloud_support@striim.com to upload the OP .scm script. Once the .scm file is uploaded, follow the steps in ‘Open Processor’ section of this recipe to configure the open processor component.

### Step 5: Set up the Slack Channel

Configure a slack channel with correct Bot Token and User Token Scopes as explained above. You can follow this link to set up the slack alerts. Generate the oauth token for your channel and configure the slack mailer component of the lag monitor app.
