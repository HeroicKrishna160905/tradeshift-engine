import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create the queue (durable=True means it survives restarts)
channel.queue_declare(queue='news_scraper_queue', durable=True)

print("✅ Queue 'news_scraper_queue' created successfully.")
connection.close()