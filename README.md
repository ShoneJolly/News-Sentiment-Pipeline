# News Sentiment Analysis & Visualization Pipeline (AWS)
This project is a fully serverless, scalable pipeline for analyzing the sentiment of real-time news articles and visualizing trends in a web dashboard. Using AWS services like Lambda, EventBridge, RDS (PostgreSQL), S3, ECS Fargate, and Docker, it automatically:

1. Fetches the latest news every 5 minutes from a News API

2. Analyzes sentiment using VADER NLP

3. Stores structured sentiment data in S3 bucket as JSON file and PostgreSQL

4. Visualizes insights in an interactive dashboard hosted on ECS

This architecture is designed to provide real-time, automated sentiment monitoring for current events and trending topics.

# Architecture Image

![Architecture](https://github.com/user-attachments/assets/31df66f4-01cb-4f35-9ab4-3bfd53aa540d)
