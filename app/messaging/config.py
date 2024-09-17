''' 
This module initialize RabbitMQ and define the consumer logic.
'''

import pika
from .listener import handle_request

# RabbitMQ connection configuration
def get_rabbitmq_connection():
    credentials = pika.PlainCredentials('user', 'password')
    return pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='/', credentials=credentials)
    )

# Start the RabbitMQ listener
def start_rabbitmq_listener():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Ensure the queue exists
    channel.queue_declare(queue='product_details_queue')

    # Start consuming messages
    channel.basic_consume(queue='product_details_queue', on_message_callback=handle_request)
    print("Product Service: RabbitMQ Listener started, waiting for messages.")
    channel.start_consuming()