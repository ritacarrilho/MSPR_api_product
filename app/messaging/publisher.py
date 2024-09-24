'''
This file handles the business logic of publishing messages in response to RabbitMQ requests.

The `publish_message` function is responsible for:
- Formatting and serializing product data into JSON.
- Publishing the response back to the requesting service using RabbitMQ.
- Logging key steps, including successful message publication and any potential errors.
'''

import pika
import asyncio
import aio_pika
import json
import logging
import os
from .service import process_stock_update_message

from dotenv import load_dotenv

load_dotenv()

BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = os.getenv('BROKER_PORT')
BROKER_VIRTUAL_HOST = os.getenv('BROKER_VIRTUAL_HOST')

def publish_message(ch, properties, products_json):
    try:
        response = json.dumps(products_json)
        logging.info(f"Publishing response: {response}")

        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=response
        )

        logging.info(f"Response published successfully for correlation_id: {properties.correlation_id}")
    except Exception as e:
        logging.error(f"Error publishing message: {e}")


async def publish_stock_update(product_id, new_quantity, order_id):
    connection = await aio_pika.connect_robust(f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}/")
    async with connection:
        channel = await connection.channel()
        stock_exchange = await channel.get_exchange('stock_exchange')
        
        message = aio_pika.Message(
            body=json.dumps({
                "event": "stock_updated",
                "product_id": product_id,
                "new_quantity": new_quantity,
                "order_id": order_id
            }).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await stock_exchange.publish(message, routing_key='products.stock_update')


async def start_stock_consumer():
    connection = await aio_pika.connect_robust(f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.get_queue('stock_update')
        await queue.consume(process_stock_update_message)
        print("Stock consumer started. Waiting for messages...")
        await asyncio.Future() 

