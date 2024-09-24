'''
This file handles the core logic of processing RabbitMQ messages in response to incoming product data requests.

The `handle_request` function is responsible for:
- Receiving messages from RabbitMQ containing product IDs.
- Validating and parsing the incoming message body.
- Fetching product details from the database based on the product IDs.
- Sending the processed product data back to the requesting service through RabbitMQ.
- Logging important events such as errors, incoming requests, and successful message handling.
- Acknowledging the message once processing is complete, or rejecting it in case of failure.
'''

import pika
import json
import json
import logging
from .service import fetch_products_by_id
from..database import get_db

# Function to handle incoming RabbitMQ messages
def handle_request(ch, method, properties, body):
    db = next(get_db())  # Get the database session from the generator
    try:
        if not body or body.strip() == "":
            logging.error("Empty or invalid message body received.")
            ch.basic_nack(delivery_tag=method.delivery_tag)
            return

        data = json.loads(body)
        product_ids = data.get('product_ids', [])
        logging.info(f"Processing product IDs: {product_ids}")
        
        products_json = fetch_products_by_id(product_ids, db)

        response = json.dumps(products_json)
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=response
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logging.info(f"Products processed and response sent for product IDs: {product_ids}")

    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e} - Raw body: {body}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error handling request: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    finally:
        db.close()