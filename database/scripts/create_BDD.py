import mysql.connector
from mysql.connector import errorcode
import json
import os

# Informations de connexion MySQL
config = {
    'user': 'root',      
    'password': '',      
    'host': 'localhost', 
}

# Nom de la base de données
db_name = 'product_db'

# Chemin du fichier JSON
# json_file_path = os.path.join('..', 'data', 'data.json')
json_file_path = os.path.join(os.getcwd(), 'database/data', 'data.json')

# Connexion à MySQL
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Suppression de la base de données si elle existe déjà
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"La base de données '{db_name}' a été supprimée.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la suppression de la base de données : {err}")

    # Création de la base de données
    try:
        cursor.execute(f"CREATE DATABASE {db_name} DEFAULT CHARACTER SET 'utf8'")
        print(f"La base de données '{db_name}' a été créée avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la création de la base de données : {err}")
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"La base de données '{db_name}' existe déjà.")
        else:
            print(err)

    # Sélectionner la base de données
    cursor.execute(f"USE {db_name}")

    # Définir les requêtes de création des tables
    create_tables_queries = {
        'Products': """
            CREATE TABLE products (
                id_product SMALLINT,
                created_at DATETIME NOT NULL,
                name VARCHAR(50) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                description VARCHAR(150),
                color VARCHAR(50) NOT NULL,
                PRIMARY KEY (id_product),
                UNIQUE (name)
            )
        """,
        'Stocks': """
            CREATE TABLE stocks (
                id_stocks SMALLINT AUTO_INCREMENT,
                quantity INT NOT NULL,
                id_product SMALLINT NOT NULL,
                PRIMARY KEY (id_stocks),
                FOREIGN KEY (id_product) REFERENCES products(id_product)
            )
        """
    }

    # Création des tables
    for table_name, create_query in create_tables_queries.items():
        try:
            cursor.execute(create_query)
            print(f"Table '{table_name}' créée avec succès.")
        except mysql.connector.Error as err:
            print(f"Erreur lors de la création de la table {table_name} : {err}")

    # Lecture des données du fichier JSON
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Insertion des données dans la table Products et Stocks
        for product in data:
            insert_product = """
                INSERT INTO products (id_product, created_at, name, price, description, color)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_product, (
                product['id'],
                product['createdAt'],
                product['name'],
                product['details']['price'],
                product['details']['description'],
                product['details']['color']
            ))

            # Insertion des données dans la table Stocks
            insert_stock = """
                INSERT INTO stocks (quantity, id_product)
                VALUES (%s, %s)
            """
            cursor.execute(insert_stock, (
                product['stock'],
                product['id']
            ))

        # Valider les changements
        cnx.commit()
        print("Données insérées avec succès.")

    except FileNotFoundError:
        print(f"Le fichier {json_file_path} n'existe pas.")
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion des données : {err}")

    # Fermer la connexion
    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    print(f"Erreur de connexion à MySQL : {err}")
