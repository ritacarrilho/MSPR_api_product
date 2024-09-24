import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.controllers import (
    get_product_by_id, create_product, update_product, delete_product,
    get_stock_by_id, create_stock, update_stock, delete_stock,
    get_category_by_id, create_category, update_category, delete_category
)
from app.models import Product, Stock, Category
from app.schemas import (
    ProductCreate, ProductUpdate, StockCreate, StockUpdate, CategoryCreate, CategoryUpdate
)
from datetime import datetime

class TestProductController(unittest.TestCase):

    def setUp(self):
        # Set up a mock database session for each test
        self.db = MagicMock(spec=Session)

    # --------------------- Product Tests --------------------- #

    # def test_get_products(self):
    #     mock_products = [Product(id_product=1, name="Product 1"), Product(id_product=2, name="Product 2")]
    #     self.db.query().all.return_value = mock_products

    #     result = get_products(self.db)
    #     self.db.query.assert_called_once_with(Product)
    #     self.db.query().all.assert_called_once()

    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].name, "Product 1")
    #     self.assertEqual(result[1].name, "Product 2")

    def test_get_product_by_id(self):
        mock_product = Product(id_product=1, name="Product 1")
        self.db.query().filter().first.return_value = mock_product

        result = get_product_by_id(self.db, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.name, "Product 1")

    def test_create_product(self):
        product_create = ProductCreate(
            name="New Product",
            price=12.99,
            description="Description of new product",
            origin="Colombia",
            created_at=datetime.now()
        )

        result = create_product(self.db, product_create)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_product(self):
        mock_product = Product(id_product=1, name="Old Product")
        self.db.query().filter().first.return_value = mock_product

        product_update = ProductUpdate(name="Updated Product", price=15.99)

        result = update_product(self.db, 1, product_update)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.name, "Updated Product")
        self.assertEqual(result.price, 15.99)

    # def test_delete_product(self):
    #     # Simuler un produit à supprimer
    #     product_to_delete = Product(id_product=1, name="Product 1", price=100)
    #     self.db.query().filter_by().first.return_value = product_to_delete

    #     # Appeler la fonction delete_product
    #     result = delete_product(self.db, 1)

    #     # Vérifier que la méthode delete a été appelée sur le produit
    #     self.db.delete.assert_called_once_with(product_to_delete)

    #     # Vérifier que l'objet supprimé n'existe plus
    #     self.db.query().filter_by().first.return_value = None
    #     deleted_product = self.db.query(Product).filter_by(id_product=1).first()
    #     self.assertIsNone(deleted_product)


    # --------------------- Stock Tests --------------------- #

    # def test_get_stocks(self):
    #     mock_stocks = [Stock(id_stock=1, quantity=100, id_product=1), Stock(id_stock=2, quantity=50, id_product=2)]
    #     self.db.query().all.return_value = mock_stocks

    #     result = get_stocks(self.db)
    #     self.db.query.assert_called_once_with(Stock)
    #     self.db.query().all.assert_called_once()

    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].quantity, 100)
    #     self.assertEqual(result[1].quantity, 50)

    def test_get_stock_by_id(self):
        mock_stock = Stock(id_stocks=1, quantity=100, id_product=1)
        self.db.query().filter().first.return_value = mock_stock

        result = get_stock_by_id(self.db, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.quantity, 100)

    def test_create_stock(self):
        stock_create = StockCreate(
            quantity=100,
            id_product=1,
            created_at=datetime.now()
        )

        result = create_stock(self.db, stock_create)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_update_stock(self):
        mock_stock = Stock(id_stocks=1, quantity=100, id_product=1)
        self.db.query().filter().first.return_value = mock_stock

        stock_update = StockUpdate(quantity=150)

        result = update_stock(self.db, 1, stock_update)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.quantity, 150)

    # def test_delete_stock(self):
    #     # Simuler un stock à supprimer
    #     stock_to_delete = Stock(id_stock=1, quantity=100, id_product=1)
    #     self.db.query().filter_by().first.return_value = stock_to_delete

    #     # Appeler la fonction delete_stock
    #     result = delete_stock(self.db, 1)

    #     # Vérifier que le stock a été supprimé
    #     self.db.query().filter_by().delete.assert_called_once()
        
    #     # Vérifier que l'objet supprimé n'existe plus
    #     self.db.query().filter_by().first.return_value = None
    #     deleted_stock = self.db.query(Stock).filter_by(id_stock=1).first()
    #     self.assertIsNone(deleted_stock)


    # --------------------- Category Tests --------------------- #

    # def test_get_categories(self):
    #     mock_categories = [Category(id_category=1, name="Category 1"), Category(id_category=2, name="Category 2")]
    #     self.db.query().all.return_value = mock_categories

    #     result = get_categories(self.db)
    #     self.db.query.assert_called_once_with(Category)
    #     self.db.query().all.assert_called_once()

    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].name, "Category 1")
    #     self.assertEqual(result[1].name, "Category 2")

    def test_get_category_by_id(self):
        mock_category = Category(id_category=1, name="Category 1")
        self.db.query().filter().first.return_value = mock_category

        result = get_category_by_id(self.db, 1)
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.name, "Category 1")

    # def test_create_category(self):
    #     category_create = CategoryCreate(
    #         name="New Category",
    #         description="Description of new category"
    #     )

    #     result = create_category(self.db, category_create)
    #     self.db.add.assert_called_once()
    #     self.db.commit.assert_called_once()
    #     self.db.refresh.assert_called_once()

    def test_update_category(self):
        mock_category = Category(id_category=1, name="Old Category")
        self.db.query().filter().first.return_value = mock_category

        category_update = CategoryUpdate(name="Updated Category")

        result = update_category(self.db, 1, category_update)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertEqual(result.name, "Updated Category")

    # def test_delete_category(self):
    #     mock_category = Category(id_category=1, name="Category 1")
    #     self.db.query().filter().first.return_value = mock_category

    #     result = delete_category(self.db, 1)
    #     self.db.delete.assert_called_once_with(mock_category)
    #     self.db.commit.assert_called_once()
    #     self.assertEqual(result.name, "Category 1")


if __name__ == '__main__':
    unittest.main()
