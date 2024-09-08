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
