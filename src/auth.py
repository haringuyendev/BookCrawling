import json
import os
from loguru import logger
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

from config.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, USERS_FILE


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_users(self):
        with open(USERS_FILE, "w") as file:
            json.dump(self.users, file, indent=4)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_access_token(self, token: str) -> dict:
        try:
            logger.info(token)
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            logger.info("Payload:", payload)  # Log payload
            return payload
        except jwt.PyJWTError as e:
            logger.error(f"JWT Error: {str(e)}")
            return None

    def get_user(self, username: str):
        return self.users.get(username)

    def create_user(self, username: str, password: str):
        hashed_password = self.hash_password(password)
        self.users[username] = {
            "username": username,
            "hashed_password": hashed_password
        }
        self.save_users()

    