from typing import Optional
from fastapi import Depends, Header, HTTPException, Request
from db.database import get_db
from db.models import User
from sqlalchemy.orm import Session
from .jwt import verify_access_token
from .api_keys import verify_api_key

class UserContext:
    def __init__(self, user_id: str, email: str, role: str):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.tier = role  # For backward compatibility

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(default=None),
    x_api_key: Optional[str] = Header(default=None)
) -> UserContext:
    """Get current user from JWT token or API key"""
    
    # Try API key first
    if x_api_key:
        user = verify_api_key(x_api_key, db)
        if user:
            user_context = UserContext(
                user_id=user.id,
                email=user.email,
                role=user.role
            )
            # Set user tier in request state for Prometheus metrics
            request.state.user_tier = user.role
            return user_context
    
    # Try JWT token
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            payload = verify_access_token(token)
            user_id = payload.get("sub")
            email = payload.get("email")
            role = payload.get("role", "free")
            
            # Verify user still exists in database
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            
            user_context = UserContext(
                user_id=user.id,
                email=user.email,
                role=user.role
            )
            # Set user tier in request state for Prometheus metrics
            request.state.user_tier = user.role
            return user_context
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    # Fallback to header-based auth for development
    x_user_id = request.headers.get("X-User-Id")
    x_user_tier = request.headers.get("X-User-Tier", "free")
    
    if x_user_id:
        user_context = UserContext(
            user_id=x_user_id,
            email=f"{x_user_id}@dev.local",
            role=x_user_tier
        )
        # Set user tier in request state for Prometheus metrics
        request.state.user_tier = x_user_tier
        return user_context
    
    raise HTTPException(status_code=401, detail="Authentication required")
