from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User, Usage, Plan
from metrics.usage import get_user_usage_summary, log_usage
from auth.dependencies import get_current_user, UserContext
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from pydantic import BaseModel

router = APIRouter()

# Response models
class UsageSummary(BaseModel):
    user_id: str
    email: str
    role: str
    total_requests: int
    total_tokens_in: int
    total_tokens_out: int
    total_cost: float
    feature_breakdown: dict

class CostSummary(BaseModel):
    total_cost: float
    cost_by_provider: dict
    cost_by_feature: dict
    cost_by_tier: dict
    period_days: int

class LeaderboardEntry(BaseModel):
    user_id: str
    email: str
    role: str
    requests: int
    tokens: int
    cost: float

def require_admin(current_user: UserContext = Depends(get_current_user)):
    """Require admin role"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/usage/summary")
async def get_usage_summary(
    user_id: Optional[str] = Query(None),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    admin: UserContext = Depends(require_admin)
):
    """Get usage summary for a specific user or all users"""
    if user_id:
        # Get specific user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        summary = get_user_usage_summary(user_id, days, db)
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            },
            "usage": summary
        }
    else:
        # Get all users summary
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all users with usage in the period
        users_with_usage = db.query(User).join(Usage).filter(
            Usage.created_at >= start_date
        ).distinct().all()
        
        summaries = []
        for user in users_with_usage:
            summary = get_user_usage_summary(user.id, days, db)
            summaries.append({
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                },
                "usage": summary
            })
        
        return {"users": summaries}

@router.get("/usage/leaderboard")
async def get_usage_leaderboard(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: UserContext = Depends(require_admin)
):
    """Get usage leaderboard"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Aggregate usage by user
    usage_stats = db.query(
        Usage.user_id,
        func.count(Usage.id).label('requests'),
        func.sum(Usage.tokens_in + Usage.tokens_out).label('tokens'),
        func.sum(Usage.cost_usd).label('cost')
    ).filter(
        Usage.created_at >= start_date
    ).group_by(Usage.user_id).order_by(desc('requests')).limit(limit).all()
    
    # Get user details
    leaderboard = []
    for stat in usage_stats:
        user = db.query(User).filter(User.id == stat.user_id).first()
        if user:
            leaderboard.append(LeaderboardEntry(
                user_id=user.id,
                email=user.email,
                role=user.role,
                requests=stat.requests,
                tokens=stat.tokens or 0,
                cost=float(stat.cost or 0)
            ))
    
    return {"leaderboard": leaderboard}

@router.get("/costs")
async def get_cost_summary(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    admin: UserContext = Depends(require_admin)
):
    """Get cost breakdown by provider, feature, and tier"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Total cost
    total_cost = db.query(func.sum(Usage.cost_usd)).filter(
        Usage.created_at >= start_date
    ).scalar() or 0.0
    
    # Cost by provider
    cost_by_provider = db.query(
        Usage.provider,
        func.sum(Usage.cost_usd).label('cost')
    ).filter(
        Usage.created_at >= start_date
    ).group_by(Usage.provider).all()
    
    # Cost by feature
    cost_by_feature = db.query(
        Usage.feature,
        func.sum(Usage.cost_usd).label('cost')
    ).filter(
        Usage.created_at >= start_date
    ).group_by(Usage.feature).all()
    
    # Cost by tier
    cost_by_tier = db.query(
        User.role,
        func.sum(Usage.cost_usd).label('cost')
    ).join(Usage).filter(
        Usage.created_at >= start_date
    ).group_by(User.role).all()
    
    return CostSummary(
        total_cost=float(total_cost),
        cost_by_provider={row.provider: float(row.cost) for row in cost_by_provider},
        cost_by_feature={row.feature: float(row.cost) for row in cost_by_feature},
        cost_by_tier={row.role: float(row.cost) for row in cost_by_tier},
        period_days=days
    )

@router.get("/users")
async def list_users(
    role: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    admin: UserContext = Depends(require_admin)
):
    """List users with optional role filter"""
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.limit(limit).all()
    
    return {
        "users": [
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at
            }
            for user in users
        ]
    }
