from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "demo-secret-key"
ALGORITHM = "HS256"


def create_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=2),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
