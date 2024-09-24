import os
import unittest
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from jose import JWTError, jwt
from app.middleware import verify_jwt_token, get_current_user, is_admin, is_customer_or_admin

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'application FastAPI pour les tests
app = FastAPI()

# Simuler un endpoint qui utilise le middleware
@app.get("/test-admin")
def test_admin(current_user: dict = Depends(get_current_user)):
    is_admin(current_user)
    return {"message": "Access granted"}

@app.get("/test-customer/{customer_id}")
def test_customer(customer_id: int, current_user: dict = Depends(get_current_user)):
    is_customer_or_admin(current_user, customer_id)
    return {"message": "Access granted"}

# Fonction pour générer un token JWT valide
def create_access_token(data: dict):
    secret_key = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    return jwt.encode(data, secret_key, algorithm=algorithm)

class TestMiddleware(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_verify_jwt_token_valid(self):
        # Simuler un token JWT valide
        token_data = {"id_customer": 1, "customer_type": 1}
        token = create_access_token(token_data)

        # Appeler la fonction verify_jwt_token
        payload = verify_jwt_token(token)
        self.assertEqual(payload["id_customer"], 1)
        self.assertEqual(payload["customer_type"], 1)

    def test_verify_jwt_token_invalid(self):
        with self.assertRaises(HTTPException) as context:
            verify_jwt_token("invalid_token")
        self.assertEqual(context.exception.status_code, 401)

    def test_admin_access(self):
        token_data = {"id_customer": 1, "customer_type": 1}
        token = create_access_token(token_data)
        
        response = self.client.get("/test-admin", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Access granted"})

    def test_admin_access_forbidden(self):
        token_data = {"id_customer": 2, "customer_type": 0}  # Non-admin user
        token = create_access_token(token_data)

        response = self.client.get("/test-admin", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "You do not have the necessary permissions to access this resource")

    def test_customer_access(self):
        token_data = {"id_customer": 1, "customer_type": 1}
        token = create_access_token(token_data)

        response = self.client.get("/test-customer/1", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Access granted"})

    def test_customer_access_forbidden(self):
        token_data = {"id_customer": 2, "customer_type": 0}  # Non-admin user
        token = create_access_token(token_data)

        response = self.client.get("/test-customer/1", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "You do not have permission to access this resource")

if __name__ == "__main__":
    unittest.main()
