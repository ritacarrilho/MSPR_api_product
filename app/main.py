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

## requête GET en plus possible 
## Obtenir les produits avec leur stock
## Obtenir les produits par couleur
## Obtenir les produits avec un prix inférieur à une valeur spécifiée
## Obtenir le stock total pour chaque produit
## Obtenir les produits créés après une certaine date

@app.post("/products/", response_model=schemas.Product, tags=["products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.post("/stocks/", response_model=schemas.Stock, tags=["stocks"])
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    db_stock = models.Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

@app.patch("/products/{id}", response_model=schemas.Product, tags=["products"])
def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = controllers.update_product(db, id, product)
    return db_product

@app.patch("/stocks/{id}", response_model=schemas.Stock, tags=["stocks"])
def update_stock(id: int, stock: schemas.StockUpdate, db: Session = Depends(get_db)):
    db_stock = controllers.update_stock(db, id, stock)
    return db_stock

@app.delete("/products/{id}", tags=["products"])
def delete_product(id: int, db: Session = Depends(get_db)):
    """
    Supprime un produit de la base de données.

    Args:
        id (int): L'ID du produit à supprimer.
        db (Session): La session de base de données.

    Returns:
        dict: Message de confirmation.
    """
    controllers.delete_product(db, id)
    return {"detail": "Product deleted"}

@app.delete("/stocks/{id}", tags=["stocks"])
def delete_stock(id: int, db: Session = Depends(get_db)):
    """
    Supprime un stock de la base de données.

    Args:
        id (int): L'ID du stock à supprimer.
        db (Session): La session de base de données.

    Returns:
        dict: Message de confirmation.
    """
    controllers.delete_stock(db, id)
    return {"detail": "Stock deleted"}