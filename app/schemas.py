from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    created_at: datetime
    update_at : datetime
    name: str
    price: float
    description: Optional[str] = None
    origin : str

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
        
class ProductUpdate(BaseModel):
    created_at: Optional[datetime] = None
    update_at : Optional[datetime] = None
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    origin : Optional[str] = None

    class Config:
        orm_mode = True

class StockUpdate(BaseModel):
    quantity: Optional[int] = None
    id_product: Optional[int] = None

    class Config:
        orm_mode = True