from sqlalchemy.orm import Session
from .models import Product, Stock, Category, Supplier, ProductSupplier
from fastapi import HTTPException
from .schemas import ProductCreate, StockCreate, ProductUpdate, StockUpdate, CategoryCreate, CategoryUpdate, SupplierCreate, SupplierUpdate, ProductSupplierCreate

# --------------------- Products & Stocks Controllers --------------------- #

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id_product == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_all_stocks(db: Session):
    return db.query(Stock).all()

def get_products_by_ids(db: Session, product_ids: list):
    if not product_ids:
        raise ValueError("Product IDs list is empty")

    products = db.query(Product).filter(Product.id_product.in_(product_ids)).all()

    if not products:
        raise ValueError("No products found for the given IDs")

    return products

def get_products_by_id(db: Session, product_ids: list):
    products = db.query(Product).filter(Product.id_product.in_(product_ids)).all()
    
    if not products:
        raise HTTPException(status_code=404, detail="No products found for the given IDs")

    return products

def get_stock_by_id(db: Session, stock_id: int):
    stock = db.query(Stock).filter(Stock.id_stocks == stock_id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

def get_product_stock(db: Session, id: int):
    stocks = db.query(Stock).filter(Stock.id_product == id).all()
    if not stocks:
        raise HTTPException(status_code=404, detail="No stock found for this product")
    return stocks

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_stock(db: Session, stock: StockCreate):
    db_stock = Stock(**stock.dict(exclude_unset=True))
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    db_product = db.query(Product).filter(Product.id_product == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

def update_stock(db: Session, stock_id: int, stock_data: StockUpdate):
    db_stock = db.query(Stock).filter(Stock.id_stocks == stock_id).first()
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")

    update_data = stock_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_stock, key, value)

    db.commit()
    db.refresh(db_stock)
    return db_stock

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id_product == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()

def delete_stock(db: Session, stock_id: int):
    db_stock = db.query(Stock).filter(Stock.id_stocks == stock_id).first()
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")

    db.delete(db_stock)
    db.commit()
    
# --------------------- Categories Controllers --------------------- #

def get_all_categories(db: Session):
    return db.query(Category).all()

def get_category_by_id(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id_category == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_data: CategoryUpdate):
    db_category = db.query(Category).filter(Category.id_category == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = category_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id_category == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()

# --------------------- Suppliers Controllers --------------------- #
def get_all_suppliers(db: Session):
    return db.query(Supplier).all()

def get_supplier_by_id(db: Session, supplier_id: int):
    supplier = db.query(Supplier).filter(Supplier.id_supplier == supplier_id).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

def create_supplier(db: Session, supplier: SupplierCreate):
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def update_supplier(db: Session, supplier_id: int, supplier_data: SupplierUpdate):
    db_supplier = db.query(Supplier).filter(Supplier.id_supplier == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    update_data = supplier_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_supplier, key, value)

    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session, supplier_id: int):
    db_supplier = db.query(Supplier).filter(Supplier.id_supplier == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    db.delete(db_supplier)
    db.commit()

# --------------------- Product suppliers Controllers --------------------- #
def get_all_product_suppliers(db: Session):
    return db.query(ProductSupplier).all()

def get_product_supplier(db: Session, product_id: int, supplier_id: int):
    product_supplier = db.query(ProductSupplier).filter(
        ProductSupplier.id_product == product_id,
        ProductSupplier.id_supplier == supplier_id
    ).first()
    if product_supplier is None:
        raise HTTPException(status_code=404, detail="Product-Supplier relation not found")
    return product_supplier

def create_product_supplier(db: Session, product_supplier: ProductSupplierCreate):
    db_product_supplier = ProductSupplier(**product_supplier.dict())
    db.add(db_product_supplier)
    db.commit()
    db.refresh(db_product_supplier)
    return db_product_supplier

def delete_product_supplier(db: Session, product_id: int, supplier_id: int):
    product_supplier = db.query(ProductSupplier).filter(
        ProductSupplier.id_product == product_id,
        ProductSupplier.id_supplier == supplier_id
    ).first()
    if product_supplier is None:
        raise HTTPException(status_code=404, detail="Product-Supplier relation not found")

    db.delete(product_supplier)
    db.commit()
