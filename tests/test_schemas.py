import unittest
from datetime import datetime
from pydantic import ValidationError
from app.schemas import (
    ProductCreate, ProductUpdate, StockCreate, StockUpdate,
    CategoryCreate, CategoryUpdate, SupplierCreate, SupplierUpdate
)

# Test de sérialisation et validation des types
class TestSchemas(unittest.TestCase):

    def setUp(self):
        # Données valides pour les tests
        self.valid_product_data = {
            "created_at": datetime.now(),
            "name": "Café Arabica",
            "price": 12.99,
            "description": "Café de haute qualité.",
            "origin": "Colombie"
        }

        self.valid_stock_data = {
            "quantity": 100,
            "id_product": 1,
            "created_at": datetime.now()
        }

        self.valid_category_data = {
            "name": "Café",
            "description": "Catégorie de café.",
            "id_product": 1
        }

        self.valid_supplier_data = {
            "name": "Fournisseur Café",
            "siret": "123456789",
            "address": "123 Rue du Café",
            "email": "contact@fournisseurcafe.com",
            "phone": "0123456789",
            "created_at": datetime.now()
        }

    # Product tests
    def test_create_product_valid_data(self):
        product = ProductCreate(**self.valid_product_data)
        self.assertEqual(product.name, "Café Arabica")
        self.assertEqual(product.price, 12.99)

    def test_update_product_optional_fields(self):
        product_update = ProductUpdate(name="Café Robusta", price=10.99)
        self.assertEqual(product_update.name, "Café Robusta")
        self.assertEqual(product_update.price, 10.99)
        self.assertIsNone(product_update.origin)

    # Stock tests
    def test_create_stock_valid_data(self):
        stock = StockCreate(**self.valid_stock_data)
        self.assertEqual(stock.quantity, 100)
        self.assertEqual(stock.id_product, 1)

    def test_update_stock_optional_fields(self):
        stock_update = StockUpdate(quantity=150)
        self.assertEqual(stock_update.quantity, 150)
        self.assertIsNone(stock_update.id_product)

    # Category tests
    def test_create_category_valid_data(self):
        category = CategoryCreate(**self.valid_category_data)
        self.assertEqual(category.name, "Café")
        self.assertEqual(category.id_product, 1)

    def test_update_category_optional_fields(self):
        category_update = CategoryUpdate(description="Nouvelle description")
        self.assertEqual(category_update.description, "Nouvelle description")
        self.assertIsNone(category_update.name)

    # Supplier tests
    def test_create_supplier_valid_data(self):
        supplier = SupplierCreate(**self.valid_supplier_data)
        self.assertEqual(supplier.name, "Fournisseur Café")
        self.assertEqual(supplier.siret, "123456789")

    def test_update_supplier_optional_fields(self):
        supplier_update = SupplierUpdate(email="nouveau_contact@fournisseurcafe.com")
        self.assertEqual(supplier_update.email, "nouveau_contact@fournisseurcafe.com")
        self.assertIsNone(supplier_update.address)

if __name__ == "__main__":
    unittest.main()
