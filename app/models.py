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

    # Relation avec ProductSupplier
    suppliers = relationship("ProductSupplier", back_populates="product")

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


class Supplier(Base):
    __tablename__ = 'suppliers'

    id_supplier = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    siret = Column(String(80), unique=True, nullable=False)
    address = Column(String(150))
    email = Column(String(50))
    phone = Column(String(50))
    created_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime)
    
    products = relationship("ProductSupplier", back_populates="supplier")

class ProductSupplier(Base):
    __tablename__ = 'product_suppliers'

    id_product = Column(Integer, ForeignKey("products.id_product"), primary_key=True)
    id_supplier = Column(Integer, ForeignKey("suppliers.id_supplier"), primary_key=True)

    product = relationship("Product", back_populates="suppliers")
    supplier = relationship("Supplier", back_populates="products")
