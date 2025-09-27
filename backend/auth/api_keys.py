import hashlib
import secrets
from typing import Optional
from fastapi import HTTPException, status
from db.database import get_db
from db.models import ApiKey, User
from sqlalchemy.orm import Session

def generate_api_key() -> str:
    """Generate a new API key"""
    return f"taelio_{secrets.token_urlsafe(32)}"

def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()

def verify_api_key(api_key: str, db: Session) -> Optional[User]:
    """Verify an API key and return the associated user"""
    if not api_key.startswith("taelio_"):
        return None
    
    key_hash = hash_api_key(api_key)
    
    # Find the API key in database
    db_key = db.query(ApiKey).filter(
        ApiKey.key_hash == key_hash,
        ApiKey.revoked_at.is_(None)  # Not revoked
    ).first()
    
    if not db_key:
        return None
    
    # Update last used timestamp
    from datetime import datetime
    db_key.last_used_at = datetime.utcnow()
    db.commit()
    
    # Return the associated user
    return db_key.user

def create_api_key(user_id: str, name: str, db: Session) -> str:
    """Create a new API key for a user"""
    api_key = generate_api_key()
    key_hash = hash_api_key(api_key)
    
    db_key = ApiKey(
        user_id=user_id,
        key_hash=key_hash,
        name=name
    )
    db.add(db_key)
    db.commit()
    
    return api_key

def revoke_api_key(api_key_id: str, user_id: str, db: Session) -> bool:
    """Revoke an API key"""
    from datetime import datetime
    
    db_key = db.query(ApiKey).filter(
        ApiKey.id == api_key_id,
        ApiKey.user_id == user_id,
        ApiKey.revoked_at.is_(None)
    ).first()
    
    if not db_key:
        return False
    
    db_key.revoked_at = datetime.utcnow()
    db.commit()
    return True

def list_user_api_keys(user_id: str, db: Session):
    """List all API keys for a user"""
    return db.query(ApiKey).filter(
        ApiKey.user_id == user_id,
        ApiKey.revoked_at.is_(None)
    ).all()
