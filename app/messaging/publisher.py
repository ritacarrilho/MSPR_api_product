'''
This file handles the business logic of publishing messages in response to RabbitMQ requests.

The `publish_message` function is responsible for:
- Formatting and serializing product data into JSON.
- Publishing the response back to the requesting service using RabbitMQ.
- Logging key steps, including successful message publication and any potential errors.
'''

import pika
import json
import logging

def publish_message(ch, properties, products_json):
    try:
        # Convert the products data to JSON format
        response = json.dumps(products_json)
        logging.info(f"Publishing response: {response}")

        # Send the response back using RabbitMQ
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=response
        )

        logging.info(f"Response published successfully for correlation_id: {properties.correlation_id}")
    except Exception as e:
        logging.error(f"Error publishing message: {e}")