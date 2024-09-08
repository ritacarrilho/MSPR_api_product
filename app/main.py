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

@app.get("/stocks/", response_model=List[schemas.Stock], tags=["stocks"])
def get_all_stocks(db: Session = Depends(get_db)):
    return db.query(models.Stock).all()

@app.get("/stocks/{id}", response_model=schemas.Stock, tags=["stocks"])
def get_stock(id: int, db: Session = Depends(get_db)):
    stock = db.query(models.Stock).filter(models.Stock.id_stocks == id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@app.get("/products/{id}/stock", response_model=List[schemas.Stock], tags=["stocks"])
def get_product_stock(id: int, db: Session = Depends(get_db)):
    stocks = db.query(models.Stock).filter(models.Stock.id_product == id).all()
    if not stocks:
        raise HTTPException(status_code=404, detail="No stock found for this product")
    return stocks
