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

# 1. Fetching News Articles from News API
The pipeline begins by programmatically retrieving the latest news articles from a third-party News API. This API provides real-time access to headlines and stories, which serve as the raw input for sentiment analysis.

# 2. AWS Lambda – News Ingestion and Sentiment Analysis

The AWS Lambda function acts as the core processing engine, performing several tasks:

a). Loads news articles via HTTP requests from the News API.

b). Processes each article using VADER SentimentIntensityAnalyzer to generate sentiment scores (positive, negative, neutral, compound).

![1 0](https://github.com/user-attachments/assets/17cb69fa-7c6f-43ba-8dd9-616e1ed4035b)

# 3. EventBridge – Scheduled Trigger

AWS EventBridge is configured to trigger the Lambda function every 5 minutes. This ensures the system continuously pulls fresh news data without manual intervention, enabling near real-time sentiment updates.

![3 0](https://github.com/user-attachments/assets/2851a0fc-f467-426e-bb08-a95b61db327f)



