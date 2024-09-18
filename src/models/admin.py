# src/models/admin.py
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Admin:
    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def create_admin(email, password):
        password_hash = pwd_context.hash(password)
        admin = {
            'email': email,
            'password_hash': password_hash
        }
        return admin

    @staticmethod
    def verify_password(password, password_hash):
        return pwd_context.verify(password, password_hash)
