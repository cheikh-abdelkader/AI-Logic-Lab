# auth.py
import jwt
from datetime import datetime, timedelta, timezone

SECRET = "ACRbYHhECxPEe3Y5pp5czohjowhJmYrxP"

def create_token(email):
    payload = {
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=5)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None