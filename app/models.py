from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = 'products'

    id_product = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(150))
    color = Column(String(50), nullable=False)

    stocks = relationship("Stock", back_populates="product")


class Stock(Base):
    __tablename__ = 'stocks'

    id_stocks = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    id_product = Column(Integer, ForeignKey('products.id_product'), nullable=False)

    product = relationship("Product", back_populates="stocks")

Product.stocks = relationship("Stock", back_populates="product")