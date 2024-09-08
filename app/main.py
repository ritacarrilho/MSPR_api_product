from typing import List
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

app = FastAPI(
    title="Paye ton kawa",
    description="Le café c'est la vie",
    summary="API Produits",
    version="0.0.2",
)


@app.get("/products/", tags=["Products"])
def get_products():
    return {"get products": "ok"}


@app.get("/products/{id}", tags=["Products"])
def get_products():
    return {"get product by id": "ok"}