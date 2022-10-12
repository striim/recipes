# Recover your CDC pipeline on Striim after planned downtime or cluster failure with no loss of data
## Use Striim to recover or autoresume your data stream after server failure
	

[Link to full recipe](https://www.striim.com/tutorial/recover-your-cdc-pipeline-on-striim-after-planned-downtime-or-cluster-failure-with-no-loss-of-data/)
![Striim, schema evolution](https://github.com/striim/recipes/blob/main/CDC-pipeline-recovery/imagerecovery.png)

## Setting Up Striim app for CDC pipeline recovery</br>

### Step 1: Download the data and Sample TQL file from our github repo

You can download the TQL files for streaming app our github repository. Deploy the Striim app on your Striim server. It should have failure recovery enabled. If you are creating your app from wizard please follow the steps shown in the [recipe](https://www.striim.com/tutorial/recover-your-cdc-pipeline-on-striim-after-planned-downtime-or-cluster-failure-with-no-loss-of-data/)

### Step 2: Configure your source and target

Configure your source and Target in the striim components.

### Step 3:Run app before failover

Deploy your streaming app and run it for real-time data replication 

### Step 4: Run app after failover

Run the Striim app after Failover. Check the source and target for the recovered data
