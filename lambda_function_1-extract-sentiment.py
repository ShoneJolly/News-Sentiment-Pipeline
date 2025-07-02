import json
import os
import boto3
import requests
import re
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'[\n\r\t]', ' ', text)  # remove line breaks and tabs
    text = re.sub(r'\\u[0-9A-Fa-f]{4}', '', text)  # remove unicode escape sequences
    text = re.sub(r'\s+', ' ', text).strip()  # collapse multiple spaces
    return text

def analyze_sentiment(text):
    """Perform sentiment analysis using VADER"""
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound = sentiment_scores['compound']
    if compound >= 0.05:
        sentiment_label = 'Positive'
    elif compound <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'
    return {
        'compound': sentiment_scores['compound'],
        'positive': sentiment_scores['pos'],
        'negative': sentiment_scores['neg'],
        'neutral': sentiment_scores['neu'],
        'sentiment_label': sentiment_label
    }

def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3')
        bucket_name = "news-bucket-shone"
        output_prefix = "news_sentiment/"

        # Fetch news from NewsAPI
        api_key = os.environ.get('api_key')
        if not api_key:
            raise Exception("API key not found in environment variables.")

        url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=20&apiKey={api_key}"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"NewsAPI request failed: {response.status_code} - {response.text}")

        # Process news articles
        news_json = response.json()
        articles = [{
            "published_at": datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S"),
            "source": clean_text(article["source"]["name"]),
            "title": clean_text(article["title"]),
            "description": clean_text(article.get("description", ""))
        } for article in news_json.get("articles", [])]

        if not articles:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No articles found from NewsAPI',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            }

        # Perform sentiment analysis
        analyzed_articles = [{
            **article,
            'sentiment_label': sentiment_result['sentiment_label'],
            'sentiment_scores': {
                'compound': sentiment_result['compound'],
                'positive': sentiment_result['positive'],
                'negative': sentiment_result['negative'],
                'neutral': sentiment_result['neutral']
            }
        } for article in articles
        for sentiment_result in [analyze_sentiment(f"{article['title']} {article['description']}")]]

        # Store results directly in news_sentiment/
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"sentiment_{timestamp}.json"
        output_key = f"{output_prefix}{output_filename}"

        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=json.dumps(analyzed_articles, ensure_ascii=False),
            ContentType="application/json"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'News fetched, sentiment analysis completed, and results stored',
                'stored_file': output_key,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        }