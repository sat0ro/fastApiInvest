from typing import Dict

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict[str, str]) -> str:
    """
    Creates an access token that is valid for ACCESS_TOKEN_EXPIRE_MINUTES minutes.

    Args:
        data (Dict[str, str]): The data to encode in the token.

    Returns:
        str: The encoded token.
    """
    if not data:
        raise ValueError("data is required")

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError as e:
        raise ValueError(f"Failed to create token: {e}") from e

    return encoded_jwt
