# core/jwt.py

from jose import jwt
from datetime import datetime, timedelta
from jose import JWTError

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """
    Create a signed JWT with:
      - all the keys in `data` (e.g. "sub" and "user_id")
      - an "exp" claim
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def get_username_from_access_token(token: str) -> dict:
    """
    Decode and verify a JWT.
    Raises `JWTError` if invalid/expired.
    Returns the payload dict (including "sub" and "user_id").
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])