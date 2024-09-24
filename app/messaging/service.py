'''
This service handles the business logic for retrieving product details. It communicates with the repository (controllers)
to fetch product data from the database based on a list of product IDs. The service ensures that the data is returned in the correct JSON format, 
suitable for further processing or sending back to the requester.

Key Responsibilities:
- Validate the input product IDs, ensuring they are not empty.
- Interact with the database via the repository layer to fetch the products.
- Transform the retrieved product data into a structured JSON format, including handling necessary data type conversions (e.g., converting Decimals to floats for JSON serialization).
- Log any potential issues or errors encountered during the process.
'''

import aio_pika
import json
from ..controllers import get_products_by_id

def fetch_products_by_id(product_ids, db):
    if not product_ids:
        raise ValueError("Product IDs must not be empty")

    products = get_products_by_id(db, product_ids)

    products_json = [{"id": p.id_product, 
                      "name": p.name, 
                      "price": float(p.price),  
                      "description": p.description} for p in products]

    return products_json


async def process_stock_update_message(message: aio_pika.IncomingMessage):
    async with message.process():
        stock_data = json.loads(message.body)
        print(f"Updating stock for product {stock_data['product_id']} to {stock_data['new_quantity']}")
