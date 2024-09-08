from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, controllers
from .database import get_db

app = FastAPI(
    title="Paye ton kawa",
    description="Le café c'est la vie",
    summary="API Produits",
    version="0.0.2",
)

@app.get("/products/", response_model=List[schemas.Product], tags=["products"])
def get_products(db: Session = Depends(get_db)):
    return controllers.get_all_products(db)

@app.get("/products/{id}", response_model=schemas.Product, tags=["products"])
def get_product(id: int, db: Session = Depends(get_db)):
    return controllers.get_product_by_id(db, id)