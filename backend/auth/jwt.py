import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "taelio-api")
JWT_ISSUER = os.getenv("JWT_ISSUER", "taelio")

# Token expiration times
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

def create_access_token(user_id: str, email: str, role: str) -> str:
    """Create a short-lived access token"""
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "type": "access",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "aud": JWT_AUDIENCE,
        "iss": JWT_ISSUER
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    """Create a long-lived refresh token"""
    payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "aud": JWT_AUDIENCE,
        "iss": JWT_ISSUER
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Dict[str, Any]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def verify_access_token(token: str) -> Dict[str, Any]:
    """Verify an access token specifically"""
    payload = verify_token(token)
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    return payload

def verify_refresh_token(token: str) -> Dict[str, Any]:
    """Verify a refresh token specifically"""
    payload = verify_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    return payload
