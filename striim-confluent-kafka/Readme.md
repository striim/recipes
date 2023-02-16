# Streaming SQL on Kafka with Striim
## Data Integration and SQL-based processing for Kafka with Striim

[Link to full recipe](https://www.striim.com/tutorial/https://www.striim.com/tutorial/streaming-sql-on-kafka-with-striim/)
![Striim, Retail](https://github.com/striim/recipes/blob/main/striim-confluent-kafka/Image.png)


## Setting Up the Striim Applications </br>
### App 1: Kafka Source to Snowflake Target

### Step 1: Configure the Kafka Source Adapter
Kafka Config: 

session.timeout.ms==60000:sasl.mechanism==PLAIN: sasl.jaas.config==org.apache.kafka.common.security.plain.PlainLoginModule required username=”<API Key>”password=”<API Secret>”; :ssl.endpoint.identification.algorithm==https:security.protocol==SASL_SSL

### Step 2: Add a Continuous Query to process the output stream
select TO_STRING(data.get(“ordertime”)) as ordertime,
  TO_STRING(data.get(“orderid”)) as orderid,
  TO_STRING(data.get(“itemid”)) as itemid,
  TO_STRING(data.get(“address”)) as address
from kafkaOutputStream;

### Step 3: Configure your Snowflake target

### Step 4: Deploy and run the Striim app
### App 2: MongoDB Source to Kafka target

### Step 1: Set up your MongoDB Source

### Step 2: Add a Continuous Query to process incoming data

SELECT
TO_STRING(data.get("_id")) as id,
TO_STRING(data.get("name")) as name,
TO_STRING(data.get("property_type")) as property_type,
TO_STRING(data.get("room_type")) as room_type,
TO_STRING(data.get("bed_type")) as bed_type,
TO_STRING(data.get("minimum_nights")) as minimum_nights,
TO_STRING(data.get("cancellation_policy")) as cancellation_policy,
TO_STRING(data.get("accommodates")) as accommodates,
TO_STRING(data.get("bedrooms")) as no_of_bedrooms,
TO_STRING(data.get("beds")) as no_of_beds,
TO_STRING(data.get("number_of_reviews")) as no_of_reviews
FROM mongoOutputStream l

### Step 3: Set up the Kafka target

### Step 4: Deploy and run the app
