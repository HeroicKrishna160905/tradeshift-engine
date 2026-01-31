import pika
import json
import requests
from bs4 import BeautifulSoup
import time
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Initialize VADER Analyzer
analyzer = SentimentIntensityAnalyzer()

# Database Setup
DATABASE_URL = "postgresql://user:password@db:5432/tradeshift"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define NewsEvent Model
class NewsEvent(Base):
    __tablename__ = "news_events"

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, index=True)
    sentiment_score = Column(Float)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables (if they don't exist)
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables checked/created.")
except Exception as e:
    print(f"⚠️ Database connection warning: {e}")

def callback(ch, method, properties, body):
    """
    Callback function executed when a message is received from RabbitMQ.
    """
    db = SessionLocal()
    try:
        # Parse the JSON message
        message = json.loads(body)
        url = message.get('url')
        
        if not url:
            print("❌ Error: No URL provided in message")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        print(f"📰 Processing URL: {url}")
        
        # Fetch the URL content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title tag
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        
        # Calculate Sentiment
        sentiment_score = analyzer.polarity_scores(title)['compound']
        
        # Save to Database
        news_event = NewsEvent(
            headline=title,
            sentiment_score=sentiment_score,
            url=url
        )
        db.add(news_event)
        db.commit()
        
        # Print confirmation
        print(f"✅ Saved: {title} (Score: {sentiment_score:.2f})")
        
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    finally:
        db.close()


def main():
    """
    Main function to establish RabbitMQ connection and start consuming messages.
    """
    rabbitmq_host = 'tradeshift_rabbitmq'
    queue_name = 'news_scraper_queue'
    
    # Retry connection logic (RabbitMQ might not be ready immediately)
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            print(f"🔌 Connecting to RabbitMQ at {rabbitmq_host}... (attempt {attempt + 1}/{max_retries})")
            
            # Establish connection
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbitmq_host)
            )
            channel = connection.channel()
            
            # Declare the queue (idempotent operation)
            channel.queue_declare(queue=queue_name, durable=True)
            
            print(f"✅ Connected to RabbitMQ")
            print(f"👂 Listening on queue: {queue_name}")
            
            # Set up consumer
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
                auto_ack=False  # Manual acknowledgment
            )
            
            print("⏳ Waiting for messages. Press CTRL+C to exit.")
            
            # Start consuming
            channel.start_consuming()
            
        except pika.exceptions.AMQPConnectionError as e:
            print(f"⚠️ Connection failed: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("❌ Max retries reached. Exiting.")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down worker...")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
