from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = 'products'

    id_product = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    update_at  = Column(DateTime)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(150))
    origin = Column(String(50), nullable=False)
    
    # Relation avec Stock
    stocks = relationship("Stock", back_populates="product")
    
    # Relation avec Category
    categories = relationship("Category", back_populates="product")


class Stock(Base):
    __tablename__ = 'stocks'

    id_stocks = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    update_at = Column(DateTime)
    id_product = Column(Integer, ForeignKey('products.id_product'), nullable=False)

    product = relationship("Product", back_populates="stocks")

# Product.stocks = relationship("Stock", back_populates="product")

class Category(Base):
    __tablename__ = 'categories'

    id_category = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(150))
    id_product = Column(Integer, ForeignKey('products.id_product'), nullable=False)

    # Relation avec Product
    product = relationship("Product", back_populates="categories")
