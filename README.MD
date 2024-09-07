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

![](./assets/docs/docker.png)


## Commandes utiles
### Lancer le projet en local sans conteneurs
```java
python3 -m venv venv
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
uvicorn app.main:app --reload   
```
### Effacer fichiers DS_Store
```java
find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
```
