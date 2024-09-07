"""
Module with all the API endpoints for products management.
It includes the operations of creation, lecture, update and delete of products>
"""

from typing import List
from fastapi import FastAPI, HTTPException, Depends


app = FastAPI()

@app.get("/", response_model=dict, tags=["Health Check"])
def api_status():
    """
    Verifies the API status.

    Returns:
        dict: dict with the API status.
    """
    return {"status": "running"}



@app.get("/products/", tags=["Products"])
def get_products():
    return {"get products": "ok"}


@app.get("/products/{id}", tags=["Products"])
def get_products():
    return {"get product by id": "ok"}