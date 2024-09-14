## Kawa Products API 

## Participants 👥
- BILLARD Mélissa
- BRACCIALES-COMBAS Lola
- CARRILHO LAMEIRA Rita
- DIAGNE Sokhna

## Technologie 
- Api en [FastApi](https://fastapi.tiangolo.com/)

## Base de données

[MySQL](https://www.mysql.com/fr/)

**Nom BDD** : ``product_db``

### Création de la base de donnée
```python
## De la racine 
py database/scripts/create_BDD.py
```
![](/assets/create_bdd-2.png)

### Mock initial 
```
https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/
```
*Liste de données de tous les produits.*

![](/assets/mock.png)

### Modèle Conceptuel de Données (MCD)
![](/assets/MCD-3.png)

#### Modèle Logique de Données (MLD)
![](/assets/mld-3.png)

### Détails tables

#### Table `products`
- **id_product (INT, AUTO_INCREMENT, clé primaire)** : Identifiant unique pour chaque produit.
- **created_at (DATETIME, NOT NULL)** : Date et heure de création du produit.
- **update_at (DATETIME)** : Date et heure de la dernière mise à jour du produit.
- **name (VARCHAR(50), NOT NULL)** : Nom du produit.
- **price (DECIMAL(10, 2), NOT NULL)** : Prix du produit.
- **description (VARCHAR(150))** : Description du produit.
- **origin (VARCHAR(50), NOT NULL)** : Origine du produit (pays ou région d'origine).
- **UNIQUE(name)** : Contraintes d'unicité sur le nom du produit.

#### Table `stocks`
- **id_stocks (INT, AUTO_INCREMENT, clé primaire)** : Identifiant unique pour chaque enregistrement de stock.
- **quantity (INT, NOT NULL)** : Quantité en stock. Indique le nombre d'unités disponibles pour le produit référencé.
- **created_at (DATETIME)** : Date et heure de création de l'enregistrement de stock.
- **update_at (DATETIME)** : Date et heure de la dernière mise à jour de l'enregistrement de stock.
- **id_product (INT, NOT NULL)** : Référence au produit. Ce champ fait le lien avec la table `products` en stockant l'identifiant du produit correspondant.
- **FOREIGN KEY(id_product)** : Clé étrangère qui référence `id_product` dans la table `products`.

#### Table `categories`
- **id_category (INT, AUTO_INCREMENT, clé primaire)** : Identifiant unique pour chaque catégorie.
- **name (VARCHAR(50), NOT NULL)** : Nom de la catégorie.
- **description (VARCHAR(150))** : Description de la catégorie.
- **id_product (INT, NOT NULL)** : Référence au produit. Ce champ fait le lien avec la table `products` en stockant l'identifiant du produit correspondant.
- **UNIQUE(name)** : Contraintes d'unicité sur le nom de la catégorie.
- **FOREIGN KEY(id_product)** : Clé étrangère qui référence `id_product` dans la table `products`.

#### Table `suppliers`
- **id_supplier (INT, AUTO_INCREMENT, clé primaire)** : Identifiant unique pour chaque fournisseur.
- **name (VARCHAR(50), NOT NULL)** : Nom du fournisseur.
- **siret (VARCHAR(80), NOT NULL)** : Numéro SIRET du fournisseur.
- **address (VARCHAR(150))** : Adresse du fournisseur.
- **email (VARCHAR(50))** : Adresse e-mail du fournisseur.
- **phone (VARCHAR(50))** : Numéro de téléphone du fournisseur.
- **created_at (DATETIME, NOT NULL)** : Date et heure de création de l'enregistrement.
- **update_at (DATETIME)** : Date et heure de la dernière mise à jour.
- **UNIQUE(name)** : Contrainte d'unicité sur le nom du fournisseur.
- **UNIQUE(siret)** : Contrainte d'unicité sur le numéro SIRET du fournisseur.

#### Table `product_suppliers`
- **id_product (INT, NOT NULL)** : Référence au produit. Ce champ fait le lien avec la table `products` en stockant l'identifiant du produit correspondant.
- **id_supplier (INT, NOT NULL)** : Référence au fournisseur. Ce champ fait le lien avec la table `suppliers` en stockant l'identifiant du fournisseur correspondant.
- **PRIMARY KEY (id_product, id_supplier)** : Clé primaire composite qui assure l'unicité des paires produit-fournisseur.
- **FOREIGN KEY(id_product)** : Clé étrangère qui référence `id_product` dans la table `products`.
- **FOREIGN KEY(id_supplier)** : Clé étrangère qui référence `id_supplier` dans la table `suppliers`.

## Endpoints de l'API
![](/assets/api-endpoint.png)

## Docker

1) Build container : ```docker-compose build```

2) Start container : ```docker-compose up```

## Commandes utiles

### Lancer l'api en local
```python
# Dans le fichier app
fastapi dev main.py
# ou
# À la racine
 uvicorn app.main:app --reload
```

### Effacer fichiers DS_Store
```java
find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
```


