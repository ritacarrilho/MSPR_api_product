'''
This module initializes the connection to RabbitMQ and defines the retry logic for handling connection failures.

Key Responsibilities:
- Load environment variables for RabbitMQ configuration using `dotenv`.
- Implement a `get_rabbitmq_connection` function with retry logic, ensuring the application can handle transient connection issues.
- Log connection attempts, failures, and successes for easier troubleshooting.
- Provide the ability to configure the number of retries and delay between retries.
'''

import pika
import os
import logging
import time
from dotenv import load_dotenv

load_dotenv()

BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = os.getenv('BROKER_PORT')
BROKER_VIRTUAL_HOST = os.getenv('BROKER_VIRTUAL_HOST')

RETRY_DELAY = 5 
MAX_RETRIES = 5

logging.basicConfig(level=logging.INFO)

def get_rabbitmq_connection(retries=5, delay=5):
    """Attempts to connect to RabbitMQ with retry logic."""
    for attempt in range(retries):
        try:
            credentials = pika.PlainCredentials(BROKER_USER, BROKER_PASSWORD)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=BROKER_HOST, port=BROKER_PORT, virtual_host=BROKER_VIRTUAL_HOST, credentials=credentials)
            )
            logging.info("Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
    logging.error("Max retries reached. RabbitMQ connection failed.")
    return None