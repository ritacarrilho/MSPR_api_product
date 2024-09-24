import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db  
from sqlalchemy.orm import Session

DATABASE_URL_TEST = os.getenv('DATABASE_URL')  

engine = create_engine(DATABASE_URL_TEST)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_get_db(self):
        db_generator = get_db()
        db_instance = next(db_generator)
        self.assertIsInstance(db_instance, Session)

    def test_connection(self):
        try:
            connection = engine.connect()
            connection.close()
        except Exception as e:
            self.fail(f"Connection to database failed: {e}")

if __name__ == "__main__":
    unittest.main()
