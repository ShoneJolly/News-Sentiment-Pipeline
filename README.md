# News Sentiment Analysis & Visualization Pipeline (AWS)
This project is a fully serverless, scalable pipeline for analyzing the sentiment of real-time news articles and visualizing trends in a web dashboard. Using AWS services like Lambda, EventBridge, RDS (PostgreSQL), S3, ECS Fargate, and Docker, it automatically:

1. Fetches the latest news every 5 minutes from a News API.

2. Analyzes sentiment using VADER NLP.

3. Stores structured sentiment data in S3 bucket as JSON file and PostgreSQL.

4. Visualizes insights in an interactive dashboard hosted on ECS.

This architecture is designed to provide real-time, automated sentiment monitoring for current events and trending topics.

# Architecture Image

![Architecture](https://github.com/user-attachments/assets/31df66f4-01cb-4f35-9ab4-3bfd53aa540d)

# Detailed Explanation of Architecture Steps

# 1. Create API Key to Fetch News Articles from NewsAPI

Start by creating an API key that will allow your application to programmatically fetch the latest news articles.

# 2. Create AWS Lambda functions

AWS Lambda functions are created to perform the following:

Fetch articles from the News API

Process and analyze sentiment using VADER SentimentIntensityAnalyzer to generate sentiment scores (positive, negative, neutral, compound).

Store the results into S3 and RDS

This allows serverless, scalable processing without manual management of servers.

![1 0](https://github.com/user-attachments/assets/17cb69fa-7c6f-43ba-8dd9-616e1ed4035b)

# 3. Create S3 bucket to store fetched data with sentiment as JSON files

A dedicated Amazon S3 bucket is created to store the raw and processed news articles. Each file is saved in JSON format and includes:

Original article text

Sentiment scores (positive, negative, neutral, compound)

![2 0](https://github.com/user-attachments/assets/623d7b1c-4fb4-40af-8bb0-146e0c8894f2)

# 4. Create RDS (PostgreSQL)

An Amazon RDS instance with PostgreSQL is set up to store structured, queryable sentiment data. This makes it easy to generate reports and power dashboards.

# 5. Configure EventBridge and S3 trigger

AWS EventBridge is configured to trigger the Lambda function every 5 minutes. This ensures the system continuously pulls fresh news data without manual intervention, enabling near real-time sentiment updates.

![3 0](https://github.com/user-attachments/assets/2851a0fc-f467-426e-bb08-a95b61db327f)



