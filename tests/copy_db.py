import mysql.connector
from sqlalchemy import create_engine, MetaData, Table, inspect, text
from sqlalchemy.exc import SQLAlchemyError

# Configuration des connexions à la base de données
SOURCE_DB_URL = "mysql+mysqlconnector://root:@localhost:3306/product_db"
TARGET_DB_URL = "mysql+mysqlconnector://root:@localhost:3306/test_product_db"

source_engine = create_engine(SOURCE_DB_URL)
target_engine = create_engine(TARGET_DB_URL)

# Fonction pour créer la base de données cible si elle n'existe pas
def create_database_if_not_exists():
    """Crée la base de données cible si elle n'existe pas."""
    connection = mysql.connector.connect(user='root', password='', host='localhost')
    cursor = connection.cursor()
    
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS test_product_db")
        print("Base de données 'test_product_db' créée ou existe déjà.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la création de la base de données: {err}")
    finally:
        cursor.close()
        connection.close()

def copy_table(table_name):
    """Copie les données d'une table depuis la base source vers la base cible."""
    source_connection = source_engine.connect()
    target_connection = target_engine.connect()

    try:
        # Charger la table depuis la source
        print(f"Chargement de la table '{table_name}' depuis la base source...")
        source_metadata = MetaData(bind=source_engine)
        source_metadata.reflect(bind=source_engine, only=[table_name])
        table = source_metadata.tables[table_name]

        # Vérifier l'existence de la table dans la base cible
        inspector = inspect(target_engine)
        target_tables = inspector.get_table_names()

        if table_name not in target_tables:
            print(f"Création de la table '{table_name}' dans la base cible...")
            target_metadata = MetaData(bind=target_engine)
            table.create(bind=target_engine)

        # Copier les données de la table
        print(f"Copie des données de la table '{table_name}'...")
        rows = source_connection.execute(table.select()).fetchall()

        if rows:
            print(f"Premières lignes extraites : {rows[:5]}")  # Afficher les 5 premières lignes pour débogage

            insert_rows = [dict(row) for row in rows]  # Conversion en dictionnaires

            with target_connection.begin() as transaction:  # Utilisation d'une transaction pour plus de sécurité
                target_table = Table(table_name, MetaData(bind=target_engine), autoload_with=target_engine)
                insert_query = target_table.insert()
                target_connection.execute(insert_query, insert_rows)
        
        print(f"Copie de la table '{table_name}' terminée avec succès !")

    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred while copying table '{table_name}': {e}")
    except Exception as e:
        print(f"Error occurred while copying table '{table_name}': {e}")
    finally:
        source_connection.close()
        target_connection.close()

def copy_all_tables():
    """Copie toutes les tables de la base source vers la base cible."""
    create_database_if_not_exists()
    tables = ['products', 'stocks', 'categories', 'suppliers', 'product_suppliers']
    for table in tables:
        copy_table(table)

if __name__ == "__main__":
    copy_all_tables()
