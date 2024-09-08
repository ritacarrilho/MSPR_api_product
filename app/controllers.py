from sqlalchemy.orm import Session
from .models import Product
from fastapi import HTTPException

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id_product == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_all_stocks(db: Session):
    return db.query(models.Stock).all()

def get_stock_by_id(db: Session, stock_id: int):
    stock = db.query(models.Stock).filter(models.Stock.id_stocks == stock_id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock
