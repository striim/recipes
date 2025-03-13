## Real-Time Streaming Sentiment Analysis with Striim, OpenAI, and LangChain

### Ganesh Bushnam, Mahadevan Lakshminarayanan, John Kutay

In this post, we’ll walk through how to build a real-time AI-powered sentiment analysis pipeline using Striim, OpenAI, and LangChain with a simple, high-performance pipeline.

Real-time sentiment analysis is essential for applications such as monitoring and responding to customer feedback, detecting market sentiment shifts, and automating responses in conversational AI. However, implementing it often requires setting up Kafka and Spark clusters, infrastructure, message brokers, third-party data integration tools, and complex event processing frameworks, which add significant overhead, operational costs, and engineering complexity. Similarly, traditional machine learning approaches require large labeled datasets, manual feature engineering, and frequent model retraining, making them difficult to implement in real-time environments.

Striim eliminates these challenges by providing a fully integrated streaming, transformation, and AI processing platform that ingests, processes, and analyzes sentiment in real-time with minimal setup.

We’ll walk you through the design covering the following:
- Building the AI Agent using Striim’s open processor
- Using Change Data Capture (CDC) technology to capture the review contents in real-time using Striim Oracle CDC Reader.
- Grouping negative reviews in Striim partitioned windows
- Generating real-time notifications using Striim Alert Manager if the number of negative reviews exceeds threshold values and transforming them into actions for the business.

---

## Why Sentiment Analysis using Foundation Models? How is it different from Traditional Machine Learning-Based Approaches?

Sentiment analysis has traditionally relied on supervised machine learning models trained on labeled datasets, where each text sample is explicitly categorized as positive, negative, or neutral. These models typically require significant pre-processing, feature engineering, and domain-specific training to perform effectively. However, foundation models, such as large language models (LLMs), simplify sentiment analysis by leveraging their vast pretraining on diverse text corpora.

One of the key differentiators of foundation models is their unsupervised learning approach. Unlike traditional models that require labeled sentiment datasets, foundation models learn patterns, relationships, and contextual meanings from large-scale, unstructured text data without explicit supervision. This enables them to generalize sentiment understanding across multiple domains without additional training.

---

## Why Real-Time Streaming Instead of Batch Jobs?

Real-time sentiment analysis enables businesses to make swift, data-driven decisions by transforming customer feedback, social media discussions, and other textual data into actionable insights as they occur. Unlike batch-based analysis, which processes data in scheduled intervals, real-time analysis ensures that organizations can respond immediately when sentiment changes.

### Benefits of Real-Time Sentiment Analysis:
- **Instant Decision-Making:** Businesses can act on customer feedback, social media trends, and emerging issues in the moment.
- **Crisis Management:** Enables companies to intervene quickly in cases of negative publicity or brand reputation issues.
- **Enhanced Customer Experience:** Organizations can integrate with tools like Slack, Salesforce, and Microsoft Dynamics for automated alerts and responses.
- **Competitive Advantage:** Faster reaction to market sentiment gives businesses an edge over competitors relying on delayed batch analysis.
- **Dynamic Trend Monitoring:** Ensures businesses stay updated on trending topics and viral events.
- **Fraud and Risk Detection:** Detects anomalies and suspicious activities in finance and cybersecurity applications.

---

## Problem Statements

- A centralized Oracle database is used by the feedback systems.
- The business analytics team has been collecting feedback in batches and manually processing insights.
- **Real-time data synchronization:** Feedback must be captured in real-time without impacting Oracle database performance.
- **Real-time analysis:** Captured feedback must be immediately analyzed for sentiment.
- **Real-time windowing and notification:** Negative feedback should be grouped by stores, triggering notifications when thresholds are met.

---

## Solution

Striim has all the necessary features for the use case described:

- **Reader:** Capture real-time changes from Oracle database.
- **Open Processor:** AI-based sentiment analysis of review content.
- **Continuous Query (CQ):** Filters negative reviews.
- **Partitioned Window:** Groups negative reviews per store.
- **Alert Subscription:** Sends web alerts when thresholds are reached.

---

## Step-by-Step Instructions

### **Set up Striim Developer 5.0**
1. Sign up for Striim Developer Edition for free at [Striim Developer](https://signup-developer.striim.com/).
2. Select Oracle CDC as the source and Database Writer as the target in the sign-up form.

### **Prepare the Table in Oracle**
```sql
CREATE TABLE STORE_REVIEWS(
    REVIEW_ID VARCHAR(1024),
    STORE_ID VARCHAR(1024),
    REVIEW_CONTENT VARCHAR(1024)
);
```

### **Create the Striim Application**

1. Go to **Apps → Create An App → Start from Scratch** and name the app.
2. Add an **Oracle CDC Reader** to read live reviews.
3. Add an **output stream** for the AI agent.
4. Add an **Open Processor** for sentiment analysis.
5. Add a **NegativeReviewsStream** with typed fields (review_id, store_id, review_sentiment).
6. Add a **CQ** filtering negative reviews:
```sql
SELECT data[0] AS review_id, data[1] AS store_id, USERDATA(e, "reviewSentiment") AS review_verdict
FROM ReviewSentimentStream e
WHERE TO_STRING(USERDATA(e, "reviewSentiment")).toUpperCase().contains("NEGATIVE");
```
7. Add a **jumping window** to partition negative reviews by store_id.
8. Add a **NegativeReviewAlertStream** of type AlertEvent.
9. Add a **CQ** for alerts:
```sql
SELECT 'Negative Review for storeID ' + store_id, store_id + '_' + DNOW(), 'warning', 'raise',
        'Five negative reviews received for store with ID: ' + store_id
FROM NegativeReviewsWindow
GROUP BY store_id;
```
10. Add a **web alert subscription** using **NegativeReviewAlertStream**.

---

## Run the Streaming Application with AI Agent

### **Sample DML Statements**
```sql
-- Positive Review for Store 1
INSERT INTO STORE_REVIEWS VALUES(1001,'0e26a9e92e4036bfaa68eb2040a8ec97','Great customer service!');

-- Negative Reviews for Store 1
INSERT INTO STORE_REVIEWS VALUES(1004,'0e26a9e92e4036bfaa68eb2040a8ec97','Terrible experience, long lines, and rude staff.');
INSERT INTO STORE_REVIEWS VALUES(1005,'0e26a9e92e4036bfaa68eb2040a8ec97','Messy store, hard to find products.');
```
The AI agent categorizes these, and the alert system triggers notifications.

### **Additional Alert Configurations**
Alerts can be sent to **Slack** or **Teams** using [Striim Alert Subscriptions](https://www.striim.com/docs/platform/en/configuring-alerts.html).

---

## Conclusion

Experience the power of real-time sentiment analysis with Striim. Get a demo or start a free trial today to convert real-time data into actionable insights using AI techniques for enhanced customer experience and business efficiency.
