from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --------------------- Products schemas --------------------- #

class ProductBase(BaseModel):
    created_at: datetime
    update_at: Optional[datetime] = None
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
        
# --------------------- Stocks schemas --------------------- #

class Stock(BaseModel):
    quantity: int
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None
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

# --------------------- Categories schemas --------------------- #

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    id_product: int

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    id_product: Optional[int] = None

class Category(CategoryBase):
    id_category: int

    class Config:
        orm_mode = True

# --------------------- Suppliers schemas --------------------- #
# --------------------- Product suppliers schemas --------------------- #