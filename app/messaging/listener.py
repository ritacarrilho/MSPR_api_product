'''
This module initializes RabbitMQ and defines the logic for the consumer that listens for messages.

Key Responsibilities:
- Continuously attempts to connect to RabbitMQ and initialize the listener.
- If RabbitMQ is unavailable or a connection fails, the module retries the connection every 10 seconds.
- Once connected, it declares the 'product_details_e' and starts consuming messages.
- The `handle_request` function (from the consumer module) is used to process incoming messages.
- Any errors encountered during message consumption or connection are logged, and the connection is gracefully closed before retrying.
'''

import logging
import time
import aio_pika
import os
import asyncio
from .config import get_rabbitmq_connection
from .consumer import handle_request
from .service import process_stock_update_message

from dotenv import load_dotenv

load_dotenv()

BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = os.getenv('BROKER_PORT')
BROKER_VIRTUAL_HOST = os.getenv('BROKER_VIRTUAL_HOST')


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


async def start_stock_consumer():
    connection = await aio_pika.connect_robust(f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.get_queue('stock_update')
        await queue.consume(process_stock_update_message)
        print("Stock consumer started. Waiting for messages...")
        await asyncio.Future()