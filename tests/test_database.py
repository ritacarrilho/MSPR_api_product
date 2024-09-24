import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db  
from sqlalchemy.orm import Session


# Configuration de l'environnement de test
DATABASE_URL_TEST = os.getenv('DATABASE_URL')  

engine = create_engine(DATABASE_URL_TEST)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Créer un nouveau session de base de données pour chaque test
        self.db = SessionLocal()

    def tearDown(self):
        # Fermer la session après chaque test
        self.db.close()

    def test_get_db(self):
        # Test de la fonction get_db
        db_generator = get_db()
        db_instance = next(db_generator)
        self.assertIsInstance(db_instance, Session)

    def test_create_and_read_data(self):
        # Exemple de test CRUD
        # Ici, vous devriez avoir un modèle et une fonction pour ajouter des données dans la base de données
        pass  # Remplacez ceci par votre code pour créer et lire des données

    def test_connection(self):
        # Vérifiez que vous pouvez établir une connexion à la base de données de test
        try:
            connection = engine.connect()
            connection.close()
        except Exception as e:
            self.fail(f"Connection to database failed: {e}")

if __name__ == "__main__":
    unittest.main()
