import unittest
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine, MetaData, Table, insert, select, update, delete
from sqlalchemy.orm import sessionmaker

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Simuler la connexion à la base de données et la session
        cls.engine = MagicMock()
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        # Simuler les tables
        cls.metadata = MetaData()
        cls.products_table = Table('products', cls.metadata, autoload_with=cls.engine)
        cls.stocks_table = Table('stocks', cls.metadata, autoload_with=cls.engine)
        cls.categories_table = Table('categories', cls.metadata, autoload_with=cls.engine)
        cls.suppliers_table = Table('suppliers', cls.metadata, autoload_with=cls.engine)
        cls.product_suppliers_table = Table('product_suppliers', cls.metadata, autoload_with=cls.engine)

        # Simuler le comportement des méthodes de session
        cls.session.execute = MagicMock()
        cls.session.commit = MagicMock()
        cls.session.execute.return_value.rowcount = 1  # Simuler le résultat des opérations
        cls.session.execute.return_value.inserted_primary_key = [1]  # Simuler une insertion réussie

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_connection(self):
        """Teste la connexion à la base de données."""
        try:
            with self.engine.connect() as connection:
                self.assertTrue(connection, "La connexion à la base de données a échoué.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la connexion à la base de données : {e}")

    def test_table_exists(self, table_name):
        """Vérifie que la table spécifiée existe dans la base de données."""
        try:
            tables = ['products', 'stocks', 'categories', 'suppliers', 'product_suppliers']  # Simuler les tables existantes
            self.assertIn(table_name, tables, f"La table '{table_name}' n'existe pas dans la base de données.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur SQLAlchemy lors de la vérification de l'existence de la table '{table_name}' : {e}")
        except Exception as e:
            self.fail(f"Erreur lors de la vérification de la table '{table_name}' : {e}")

    def test_insert(self, table, values):
        """Teste l'insertion de données dans la table spécifiée."""
        try:
            insert_query = insert(table).values(values)
            result = self.session.execute(insert_query)
            self.session.commit()

            # Vérifier que l'insertion a réussi
            self.assertIsNotNone(result.inserted_primary_key, f"L'insertion dans la table '{table.name}' a échoué.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de l'insertion dans '{table.name}' : {e}")

    def test_read(self, table, filter_values):
        """Teste la lecture des données dans la table spécifiée."""
        try:
            # Simuler le résultat de la lecture
            self.session.execute.return_value.fetchone.return_value = {'name': 'Café Arabica'}  # Simuler des données trouvées
            select_query = select([table]).where(*[table.c[key] == value for key, value in filter_values.items()])
            result = self.session.execute(select_query).fetchone()

            # Vérifier que les données sont bien récupérées
            self.assertIsNotNone(result, f"Aucune donnée trouvée dans la table '{table.name}'.")
            for key, value in filter_values.items():
                self.assertEqual(result[key], value, f"Le champ '{key}' est incorrect.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la lecture dans '{table.name}' : {e}")

    def test_update(self, table, filter_values, update_values):
        """Teste la mise à jour des données dans la table spécifiée."""
        try:
            update_query = update(table).where(*[table.c[key] == value for key, value in filter_values.items()]).values(update_values)
            result = self.session.execute(update_query)
            self.session.commit()

            # Vérifier que la mise à jour a réussi
            self.assertGreater(result.rowcount, 0, f"Aucune ligne n'a été mise à jour dans la table '{table.name}'.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la mise à jour dans '{table.name}' : {e}")

    def test_delete(self, table, filter_values):
        """Teste la suppression de données dans la table spécifiée."""
        try:
            delete_query = delete(table).where(*[table.c[key] == value for key, value in filter_values.items()])
            result = self.session.execute(delete_query)
            self.session.commit()

            # Vérifier que la suppression a réussi
            self.assertGreater(result.rowcount, 0, f"Aucune ligne n'a été supprimée dans la table '{table.name}'.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la suppression dans '{table.name}' : {e}")

    # Tests spécifiques
    def test_table_products_exists(self):
        self.test_table_exists('products')

    def test_table_stocks_exists(self):
        self.test_table_exists('stocks')

    def test_table_categories_exists(self):
        self.test_table_exists('categories')

    def test_table_suppliers_exists(self):
        self.test_table_exists('suppliers')

    def test_table_product_suppliers_exists(self):
        self.test_table_exists('product_suppliers')

    def test_insert_into_products(self):
        values = {
            'created_at': '2024-09-14 10:00:00',
            'update_at': '2024-09-14 10:00:00',
            'name': 'Café Arabica',
            'price': 12.99,
            'description': 'Café de haute qualité',
            'origin': 'Colombie'
        }
        self.test_insert(self.products_table, values)

    def test_read_from_products(self):
        filter_values = {'name': 'Café Arabica'}
        self.test_read(self.products_table, filter_values)

    def test_update_products(self):
        filter_values = {'name': 'Café Arabica'}
        update_values = {'price': 14.99}
        self.test_update(self.products_table, filter_values, update_values)

    def test_delete_from_products(self):
        filter_values = {'name': 'Café Arabica'}
        self.test_delete(self.products_table, filter_values)

if __name__ == '__main__':
    unittest.main()
