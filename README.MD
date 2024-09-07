## Kawa Products API 

## Participants 👥
- BILLARD Mélissa
- BRACCIALES-COMBAS Lola
- CARRILHO LAMEIRA Rita

## Technologie 
- Api en [FastApi](https://fastapi.tiangolo.com/)

## Endpoints de l'API

## Docker

1) Build container : ```docker-compose build```

2) Start container : ```docker-compose up```

## Commandes utiles
### Effacer fichiers DS_Store
```java
find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
```

## Base de données

[MySQL](https://www.mysql.com/fr/)

**Nom BDD** : ``product_db``

### Mock initial 

![](/assets/mock.png)

### Modèle conceptuel de données (MCD)

### Détails tables

#### Table ``products``
id (INT, clé primaire) : Identifiant unique pour chaque produit. 

created_at (TIMESTAMP) : Date et heure de création du produit.

name (VARCHAR) : Nom du produit. 

price (DECIMAL(10, 2)) : Prix du produit. 

description (TEXT) : Description du produit. 

color (VARCHAR) : Couleur du produit. 

#### Table ``stocks``
id (INT, clé primaire) : Identifiant unique pour chaque enregistrement de stock. 

product_id (INT, clé étrangère) : Référence au produit. Ce champ fait le lien avec la table products en stockant l'identifiant du produit correspondant. Cela permet de savoir quel produit est associé à chaque enregistrement de stock.

quantity (INT) : Quantité en stock. Ce champ indique le nombre d'unités disponibles pour le produit référencé. Cela permet de gérer les niveaux de stock et de savoir quand il est nécessaire de réapprovisionner.



