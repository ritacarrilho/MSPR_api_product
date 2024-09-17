'''
This file handle the actual business logic of processing the RabbitMQ messages.
'''

import pika
import json
import json
import logging
from .service import fetch_products_by_id
from..database import get_db
from .publisher import publish_message

# Function to handle incoming RabbitMQ messages
def handle_request(ch, method, properties, body):
    db = next(get_db())  # Get the database session from the generator
    try:
        if not body or body.strip() == "":
            logging.error("Empty or invalid message body received.")
            ch.basic_nack(delivery_tag=method.delivery_tag)
            return

        # Parse incoming message
        data = json.loads(body)
        product_ids = data.get('product_ids', [])
        logging.info(f"Processing product IDs: {product_ids}")
        
        # Fetch product details
        products_json = fetch_products_by_id(product_ids, db)

        # Send the response back to the producer via RabbitMQ
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