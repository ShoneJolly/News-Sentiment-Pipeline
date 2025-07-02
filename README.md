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

![2 0](https://github.com/user-attachments/assets/3a3ef3a4-b62a-40f7-b459-53a7d2f70105)

A dedicated Amazon S3 bucket is created to store the raw and processed news articles. Each file is saved in JSON format and includes:

Original article text

Sentiment scores (positive, negative, neutral, compound)

![4 0](https://github.com/user-attachments/assets/e1ac2075-511a-4a46-9ef1-57da2e7d2c23)


# 4. Create RDS (PostgreSQL)

An Amazon RDS instance with PostgreSQL is set up to store structured, queryable sentiment data. This makes it easy to generate reports and power dashboards.

![5 0](https://github.com/user-attachments/assets/a659c05f-e202-4989-8274-ecce4c0a6485)

# 5. Configure EventBridge and S3 trigger

EventBridge:
Used to schedule the first Lambda function to run every 5 minutes, enabling regular and automated data ingestion without manual intervention.

![3 0](https://github.com/user-attachments/assets/48ab4372-7150-4560-9b4e-168952f98c33)

S3 trigger:
Configured to automatically trigger the second Lambda function whenever a new file is added to the S3 bucket, ensuring the data pipeline flows continuously into RDS.

![6 0](https://github.com/user-attachments/assets/12852971-bec6-4af6-a23a-002b5cdbd8bb)

![7 0](https://github.com/user-attachments/assets/91f3e6ea-2b9e-4065-95a1-b74ab7d3efd6)

# 6. Local development of Streamlit dashboard

A Streamlit dashboard is developed locally to visualize the sentiment data.

# 7. Create Docker container

A Docker container is built for the Streamlit dashboard. This allows consistent execution across local and cloud environments and simplifies deployment.

# 8. Push to ECR (Elastic Container Registry)

The Docker image of the Streamlit app is pushed to AWS ECR. ECR securely stores container images and integrates directly with ECS for deployment.

![8 0](https://github.com/user-attachments/assets/f51856ee-89b3-436c-9ccb-112874d0530f)

# 9. Create cluster in ECS, task definition, service, and task

An ECS cluster is created using Fargate (serverless containers).

![9 0](https://github.com/user-attachments/assets/85c1dbf5-ae01-4a2a-8367-1410f216dc72)

A task definition is set up pointing to the ECR image.

![10 0](https://github.com/user-attachments/assets/975497f0-c938-449f-bd17-62eada5be363)

A service and task are created to run and manage the container, exposing the dashboard on port 8051.

This ensures automatic scaling and management without server maintenance.

![11 0](https://github.com/user-attachments/assets/d5ac307a-e749-42bb-afb0-171df28facb3)

# 10. Web dashboard

Finally, the dashboard is accessible via a public URL or IP address mapped to the ECS service. Users can interactively explore real-time sentiment analysis results through the web interface.

![12 0](https://github.com/user-attachments/assets/2a161364-e950-4def-9c1c-f3c137bd3f08)

