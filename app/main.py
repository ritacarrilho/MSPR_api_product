from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, controllers
from .database import get_db
from.middleware import get_current_user, is_admin

app = FastAPI(
    title="Paye ton kawa",
    description="Le café c'est la vie",
    summary="API Produits",
    version="0.0.2",
)

# --------------------- Products endpoints --------------------- #

@app.get("/products/", response_model=List[schemas.Product], tags=["products"])
async def get_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve all products. Only accessible to admin users.
    """
    try:
        is_admin(current_user)
        products = controllers.get_all_products(db)
        if not products:
            raise HTTPException(status_code=404, detail="No products found")

        return products
    except HTTPException as http_exc:
        raise http_exc
    except ValueError as ve:
        print(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail="Invalid input data")
    except KeyError as ke:
        print(f"KeyError: {ke}")
        raise HTTPException(status_code=400, detail=f"Missing or invalid data: {ke}")
    except Exception as e:
        print(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving products")


@app.get("/products/{id}", response_model=schemas.Product, tags=["products"])
async def get_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve a specific product by ID. Only accessible to admin users.
    """
    try:
        is_admin(current_user)
        product = controllers.get_product_by_id(db, id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException as http_exc:
        raise http_exc
    except ValueError as ve:
        print(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail="Invalid input data")
    except KeyError as ke:
        print(f"KeyError: {ke}")
        raise HTTPException(status_code=400, detail=f"Missing or invalid data: {ke}")
    except Exception as e:
        print(f"Error fetching product with ID {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the product")


@app.post("/products/", response_model=schemas.Product, tags=["products"])
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a new product. Accessible only to admin users.
    """
    try:
        is_admin(current_user) 
        db_product = controllers.create_product(db, product)
        return db_product
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the product")


@app.patch("/products/{id}", response_model=schemas.Product, tags=["products"])
async def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Update an existing product. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        db_product = controllers.get_product_by_id(db, id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        updated_product = controllers.update_product(db, id, product)
        return updated_product
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error updating product with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the product")


@app.delete("/products/{id}", tags=["products"])
async def delete_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Delete a product from the database. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        product = controllers.get_product_by_id(db, id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        controllers.delete_product(db, id)
        return {"detail": f"Product with id {id} deleted"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error deleting product with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the product")


## requête GET en plus possible 
## Obtenir les produits avec leur stock
## Obtenir les produits avec un prix inférieur à une valeur spécifiée
## Obtenir le stock total pour chaque produit
## Obtenir les produits créés après une certaine date

# --------------------- Stocks endpoints --------------------- #

@app.get("/stocks/", response_model=List[schemas.Stock], tags=["stocks"])
async def get_all_stocks(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve all stocks. Accessible only to admin users.
    """
    try:
        is_admin(current_user) 
        stocks = controllers.get_all_stocks(db)
        if not stocks:
            raise HTTPException(status_code=404, detail="No stocks found")
        return stocks

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving stocks: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving stocks")


@app.get("/stocks/{id}", response_model=schemas.Stock, tags=["stocks"])
async def get_stock(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve a stock by ID. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        stock = controllers.get_stock_by_id(db, id)
        if stock is None:
            raise HTTPException(status_code=404, detail="Stock not found")
        return stock
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving stock with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the stock")


@app.post("/stocks/", response_model=schemas.Stock, tags=["stocks"])
async def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a new stock entry. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        db_stock = controllers.create_stock(db, stock)
        return db_stock

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating stock: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the stock")


@app.patch("/stocks/{id}", response_model=schemas.Stock, tags=["stocks"])
async def update_stock(id: int, stock: schemas.StockUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Update a stock entry. Only accessible to admin users.
    """
    try:
        is_admin(current_user)
        db_stock = controllers.get_stock_by_id(db, id)
        if not db_stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        updated_stock = controllers.update_stock(db, id, stock)
        return updated_stock

    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error updating stock with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the stock")


@app.delete("/stocks/{id}", tags=["stocks"])
async def delete_stock(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Delete a stock entry from the database. Only accessible to admin users.
    """
    try:
        is_admin(current_user)
        stock = controllers.get_stock_by_id(db, id)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        controllers.delete_stock(db, id)
        return {"detail": f"Stock with id {id} was deleted."}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error deleting stock with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the stock")


@app.get("/products/{id}/stock", response_model=List[schemas.Stock], tags=["stocks"])
async def get_product_stock(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve the stock information for a specific product. Accessible only to admin users.
    """
    try:
        is_admin(current_user) 
        stocks = controllers.get_product_stock(db, id)
        if not stocks:
            raise HTTPException(status_code=404, detail="No stock found for this product")
        return stocks
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving stock for product with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the stock information")


# --------------------- Categories endpoints --------------------- #

@app.get("/categories/", response_model=List[schemas.Category], tags=["categories"])
async def get_all_categories(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve all categories. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        categories = controllers.get_all_categories(db)
        if not categories:
            raise HTTPException(status_code=404, detail="No categories found")
        return categories

    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error retrieving categories: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving categories")


@app.get("/categories/{id}", response_model=schemas.Category, tags=["categories"])
async def get_category(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve a category by ID. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        category = controllers.get_category_by_id(db, id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        return category
    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error retrieving category with ID {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the category")


@app.post("/categories/", response_model=schemas.Category, tags=["categories"])
async def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a new category. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        new_category = controllers.create_category(db, category)
        return new_category

    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the category")


@app.patch("/categories/{id}", response_model=schemas.Category, tags=["categories"])
async def update_category(id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Update an existing category by ID. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        existing_category = controllers.get_category_by_id(db, id)

        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found")
        updated_category = controllers.update_category(db, id, category)
        return updated_category
    except HTTPException as http_exc:
        raise http_exc  
    except Exception as e:
        print(f"Error updating category with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the category")


@app.delete("/categories/{id}", tags=["categories"])
async def delete_category(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Delete a category by ID. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        category = controllers.get_category_by_id(db, id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        controllers.delete_category(db, id)
        return {"detail": f"Category with id {id} deleted successfully"}

    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error deleting category with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the category")


# --------------------- Suppliers endpoints --------------------- #
@app.get("/suppliers/", response_model=List[schemas.Supplier], tags=["suppliers"])
async def get_all_suppliers(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve all suppliers. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        suppliers = controllers.get_all_suppliers(db)
        if not suppliers:
            raise HTTPException(status_code=404, detail="No suppliers found")
        
        return suppliers
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving suppliers: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the suppliers")


@app.get("/suppliers/{id}", response_model=schemas.Supplier, tags=["suppliers"])
async def get_supplier(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve a supplier by ID. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        supplier = controllers.get_supplier_by_id(db, id)

        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return supplier
    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error retrieving supplier with ID {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the supplier")


@app.post("/suppliers/", response_model=schemas.Supplier, tags=["suppliers"])
async def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a new supplier. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        new_supplier = controllers.create_supplier(db, supplier)
        return new_supplier

    except HTTPException as http_exc:
        raise http_exc  
    except Exception as e:
        print(f"Error creating supplier: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the supplier")


@app.patch("/suppliers/{id}", response_model=schemas.Supplier, tags=["suppliers"])
async def update_supplier(id: int, supplier: schemas.SupplierUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Update an existing supplier. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        existing_supplier = controllers.get_supplier_by_id(db, id)
        if not existing_supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")

        updated_supplier = controllers.update_supplier(db, id, supplier)
        return updated_supplier
    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error updating supplier with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the supplier")


@app.delete("/suppliers/{id}", tags=["suppliers"])
async def delete_supplier(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Delete an existing supplier. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        existing_supplier = controllers.get_supplier_by_id(db, id)
        if not existing_supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        
        controllers.delete_supplier(db, id)
        return {"message": f"Supplier with id {id} was deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error deleting supplier with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the supplier")


# --------------------- Product suppliers endpoints --------------------- #
@app.get("/product_suppliers/", response_model=List[schemas.ProductSupplier], tags=["product_suppliers"])
async def get_all_product_suppliers(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve all product-supplier relationships. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        product_suppliers = controllers.get_all_product_suppliers(db)
        if not product_suppliers:
            raise HTTPException(status_code=404, detail="No product suppliers found")

        return product_suppliers
    except HTTPException as http_exc:
        raise http_exc  
    except Exception as e:
        print(f"Error retrieving product suppliers: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving product suppliers")


@app.get("/product_suppliers/{product_id}/{supplier_id}", response_model=schemas.ProductSupplier, tags=["product_suppliers"])
async def get_product_supplier(product_id: int, supplier_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve a specific product-supplier relationship. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        product_supplier = controllers.get_product_supplier(db, product_id, supplier_id)

        if not product_supplier:
            raise HTTPException(status_code=404, detail="Product-Supplier relationship not found")
        
        return product_supplier
    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error retrieving product-supplier relationship for product {product_id} and supplier {supplier_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the product-supplier relationship")


@app.post("/product_suppliers/", response_model=schemas.ProductSupplier, tags=["product_suppliers"])
async def create_product_supplier(product_supplier: schemas.ProductSupplierCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a new product-supplier relationship. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        new_product_supplier = controllers.create_product_supplier(db, product_supplier)
        return new_product_supplier
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating product-supplier relationship: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the product-supplier relationship")


@app.delete("/product_suppliers/{product_id}/{supplier_id}", tags=["product_suppliers"])
async def delete_product_supplier(product_id: int, supplier_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Delete a product-supplier relationship. Accessible only to admin users.
    """
    try:
        is_admin(current_user)
        product_supplier = controllers.get_product_supplier(db, product_id, supplier_id)
        if not product_supplier:
            raise HTTPException(status_code=404, detail="Product-Supplier relationship not found")

        controllers.delete_product_supplier(db, product_id, supplier_id)
        return {"message": "Product-Supplier relationship deleted successfully"}

    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        print(f"Error deleting product-supplier relationship: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the product-supplier relationship")

