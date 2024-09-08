from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    created_at: datetime
    name: str
    price: float
    description: Optional[str] = None
    color: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id_product: int

    class Config:
        orm_mode = True

class Stock(BaseModel):
    id_stocks: int
    quantity: int
    id_product: int

    class Config:
        orm_mode = True

class StockBase(BaseModel):
    quantity: int
    id_product: int

class StockCreate(StockBase):
    pass

class Stock(StockBase):
    id_stocks: int

    class Config:
        orm_mode = True