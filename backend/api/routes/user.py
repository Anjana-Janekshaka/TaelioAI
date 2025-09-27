from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from auth.dependencies import get_current_user, UserContext
from metrics.usage import get_user_usage_summary
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UserUsageResponse(BaseModel):
    user_id: str
    email: str
    role: str
    period_days: int
    total_requests: int
    total_tokens_in: int
    total_tokens_out: int
    total_cost: float
    feature_breakdown: dict

@router.get("/me/usage")
async def get_my_usage(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    """Get current user's usage summary"""
    summary = get_user_usage_summary(current_user.user_id, days, db)
    
    return UserUsageResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        role=current_user.role,
        period_days=days,
        total_requests=summary["total_requests"],
        total_tokens_in=summary["total_tokens_in"],
        total_tokens_out=summary["total_tokens_out"],
        total_cost=summary["total_cost"],
        feature_breakdown=summary["feature_breakdown"]
    )

@router.get("/me/profile")
async def get_my_profile(
    current_user: UserContext = Depends(get_current_user)
):
    """Get current user's profile"""
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "role": current_user.role,
        "tier": current_user.tier
    }
