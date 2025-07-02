import json
import boto3
import os
from datetime import datetime
from botocore.exceptions import ClientError
import psycopg2
from psycopg2 import sql


def get_all_sentiment_files(s3_client, bucket, prefix):
    """Get all JSON files from S3 news_sentiment folder"""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' not in response:
            raise Exception("No files found in news_sentiment folder")
        # Return all JSON file keys
        return [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.json')]
    except ClientError as e:
        raise Exception(f"Error listing S3 objects: {str(e)}")


def get_db_connection():
    """Connect to RDS PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT']
        )
        return conn
    except Exception as e:
        raise Exception(f"Database connection failed: {str(e)}")


def ensure_news_articles_table():
    """Ensure the news_articles table exists with the required schema"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_articles (
                id SERIAL PRIMARY KEY,
                published_at TIMESTAMP,
                source TEXT,
                sentiment_label TEXT,
                title TEXT,
                description TEXT
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Ensured news_articles table exists.")
    except Exception as e:
        raise Exception(f"Failed to ensure news_articles table: {str(e)}")


def clear_news_articles_table():
    """Clear all existing data from news_articles table"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM news_articles;")
        conn.commit()
        cursor.close()
        conn.close()
        print("Cleared news_articles table successfully.")
    except Exception as e:
        raise Exception(f"Failed to clear news_articles table: {str(e)}")


def insert_articles_to_db(articles):
    """Insert articles into PostgreSQL table"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        insert_query = sql.SQL("""
            INSERT INTO news_articles (published_at, source, sentiment_label, title, description)
            VALUES (%s, %s, %s, %s, %s)
        """)
        for article in articles:
            cursor.execute(insert_query, (
                article.get('published_at'),
                article.get('source'),
                article.get('sentiment_label'),
                article.get('title'),
                article.get('description')
            ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to insert articles to database: {str(e)}")


def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3')
        bucket_name = "news-bucket-shone"
        input_prefix = "news_sentiment/"

        # Ensure the table exists before proceeding
        ensure_news_articles_table()

        # Get all JSON files from news_sentiment folder
        file_keys = get_all_sentiment_files(s3_client, bucket_name, input_prefix)
        if not file_keys:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No JSON files found in news_sentiment folder',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            }

        # Clear the table before inserting new data
        clear_news_articles_table()

        processed_files = []
        inserted_count = 0

        for file_key in file_keys:
            # Read the JSON file from S3
            response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            articles = json.loads(response['Body'].read().decode('utf-8'))
            # Insert articles into RDS
            insert_articles_to_db(articles)
            inserted_count += len(articles)
            # Optionally delete the processed file (uncomment if desired)
            s3_client.delete_object(Bucket=bucket_name, Key=file_key)
            processed_files.append(file_key)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully inserted articles into RDS',
                'processed_files': processed_files,
                'db_inserted': inserted_count,
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
