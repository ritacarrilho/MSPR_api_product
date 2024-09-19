'''
This module initializes RabbitMQ and defines the logic for the consumer that listens for messages.

Key Responsibilities:
- Continuously attempts to connect to RabbitMQ and initialize the listener.
- If RabbitMQ is unavailable or a connection fails, the module retries the connection every 10 seconds.
- Once connected, it declares the 'product_details_queue' and starts consuming messages.
- The `handle_request` function (from the consumer module) is used to process incoming messages.
- Any errors encountered during message consumption or connection are logged, and the connection is gracefully closed before retrying.
'''

import logging
import time
from .config import get_rabbitmq_connection
from .consumer import handle_request

# Start the RabbitMQ listener
def start_rabbitmq_listener():
    while True:
        connection = get_rabbitmq_connection()
        if connection:
            try:
                channel = connection.channel()
                channel.queue_declare(queue='product_details_queue')
                channel.basic_consume(queue='product_details_queue', on_message_callback=handle_request)
                logging.info("RabbitMQ Listener started, waiting for messages on 'product_details_queue'.")
                channel.start_consuming()
            except Exception as e:
                logging.error(f"Error in RabbitMQ listener: {e}")
                connection.close()
        else:
            logging.error("RabbitMQ is not available. Retrying in 10 seconds...")
            time.sleep(10) 