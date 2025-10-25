from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User, Plan
from .jwt import create_access_token, create_refresh_token, verify_refresh_token
from .api_keys import create_api_key, revoke_api_key, list_user_api_keys
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from auth.dependencies import get_current_user

router = APIRouter()

# Request/Response models
class LoginRequest(BaseModel):
    email: str

class RegisterRequest(BaseModel):
    email: str
    role: str = "free"  # Default to free tier

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    email: str
    role: str
    tier: str
    limits: dict

class RefreshRequest(BaseModel):
    refresh_token: str

class ApiKeyCreateRequest(BaseModel):
    name: str

class ApiKeyResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    last_used_at: Optional[datetime]

class ApiKeyCreateResponse(BaseModel):
    api_key: str
    key_info: ApiKeyResponse

@router.post("/register", response_model=LoginResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Create new user
    user = User(
        email=request.email,
        role=request.role
    )
    db.add(user)
    db.flush()  # Get the ID
    
    # Create plan with appropriate limits
    tier_limits = {
        "free": {"requests_per_day": 50, "requests_per_minute": 2, "tokens_per_day": 10000},
        "pro": {"requests_per_day": 500, "requests_per_minute": 10, "tokens_per_day": 100000},
        "admin": {"requests_per_day": 10000, "requests_per_minute": 100, "tokens_per_day": 1000000}
    }
    
    plan = Plan(
        user_id=user.id,
        tier=request.role,
        limits_json=str(tier_limits.get(request.role, tier_limits["free"]))
    )
    db.add(plan)
    db.commit()
    
    # Generate tokens
    access_token = create_access_token(user.id, user.email, user.role)
    refresh_token = create_refresh_token(user.id)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        email=user.email,
        role=user.role,
        tier=request.role,
        limits=tier_limits.get(request.role, tier_limits["free"])
    )

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login with email (passwordless for now)"""
    # Find existing user
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    
    # Get user's plan
    plan = db.query(Plan).filter(Plan.user_id == user.id).first()
    if not plan:
        raise HTTPException(status_code=500, detail="User plan not found")
    
    # Parse limits with error handling
    import json
    try:
        limits = json.loads(plan.limits_json) if plan.limits_json else {}
    except json.JSONDecodeError:
        # Handle malformed JSON by using default limits
        limits = {"requests_per_day": 50, "requests_per_minute": 2, "tokens_per_day": 10000}
    
    # Generate tokens
    access_token = create_access_token(user.id, user.email, user.role)
    refresh_token = create_refresh_token(user.id)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        email=user.email,
        role=user.role,
        tier=plan.tier,
        limits=limits
    )

@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(request: RefreshRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        payload = verify_refresh_token(request.refresh_token)
        user_id = payload.get("sub")
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Generate new tokens
        access_token = create_access_token(user.id, user.email, user.role)
        refresh_token = create_refresh_token(user.id)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            role=user.role
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/api-keys", response_model=ApiKeyCreateResponse)
async def create_user_api_key(
    request: ApiKeyCreateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new API key for the current user"""
    api_key = create_api_key(current_user.user_id, request.name, db)
    
    # Get the created key info
    keys = list_user_api_keys(current_user.user_id, db)
    latest_key = keys[-1] if keys else None
    
    if not latest_key:
        raise HTTPException(status_code=500, detail="Failed to create API key")
    
    return ApiKeyCreateResponse(
        api_key=api_key,
        key_info=ApiKeyResponse(
            id=latest_key.id,
            name=latest_key.name,
            created_at=latest_key.created_at,
            last_used_at=latest_key.last_used_at
        )
    )

@router.get("/api-keys", response_model=List[ApiKeyResponse])
async def list_api_keys(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all API keys for the current user"""
    keys = list_user_api_keys(current_user.user_id, db)
    return [
        ApiKeyResponse(
            id=key.id,
            name=key.name,
            created_at=key.created_at,
            last_used_at=key.last_used_at
        )
        for key in keys
    ]

@router.delete("/api-keys/{key_id}")
async def revoke_user_api_key(
    key_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Revoke an API key"""
    success = revoke_api_key(key_id, current_user.user_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"message": "API key revoked successfully"}
