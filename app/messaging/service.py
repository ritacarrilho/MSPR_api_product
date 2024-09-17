'''
This service handles the business logic for retrieving product details. It interacts with the repository to fetch data and then returns it in the correct format.
'''

import json
from ..controllers import get_products_by_id


def fetch_products_by_id(product_ids, db):
    if not product_ids:
        raise ValueError("Product IDs must not be empty")

    # Fetch products using repository
    products = get_products_by_id(db, product_ids)

    # Prepare JSON response (including any necessary transformations)
    products_json = [{"id": p.id_product, 
                      "name": p.name, 
                      "price": float(p.price),  # Convert Decimal to float
                      "description": p.description} for p in products]

    return products_json