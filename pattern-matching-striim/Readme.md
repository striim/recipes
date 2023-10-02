# Detect Anomalies and Process Data Streams with Pattern Matching: A Financial Services Example
## How you can use rule-based, Complex Event Processing (CEP) to detect real world patterns in data

[Link to full recipe](https://www.striim.com/tutorial/pattern-matching-financial-data/)
![Striim, Pattern-matching](https://github.com/striim/recipes/blob/main/pattern-matching-striim/Image.png)

## Running your Pattern Matching Recipe

### Step 1: Download the data, python scripts and Sample TQL file from our github repo

You can download the TQL files for streaming app our github repository. Deploy the Striim app on your Striim server.

### Step 2: Configure your filepath (for filereader) or SQL source

Add the host name and database details for your source

### Step 3: Run the Striim App

Deploy your streaming app and run it for real-time data replication

### Step 4: Run the python script to insert the data into SQL 

To capture CDC in SQL source, run the provided python script (add your hostname and database to the script) from the same folder containing the csv file 
