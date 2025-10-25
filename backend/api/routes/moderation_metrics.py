from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Usage
from auth.dependencies import get_current_user, UserContext
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from pydantic import BaseModel

router = APIRouter()

# Response models
class ModerationMetrics(BaseModel):
    total_content_moderated: int
    total_violations_found: int
    total_unsafe_content: int
    average_safety_score: float
    violations_by_type: dict
    content_by_type: dict
    safety_score_distribution: dict
    period_days: int

class ModerationViolation(BaseModel):
    violation_type: str
    count: int
    severity: str
    percentage: float

class ModerationStats(BaseModel):
    user_id: str
    period_days: int
    total_moderations: int
    violations_found: int
    unsafe_content_count: int
    average_safety_score: float
    violation_breakdown: List[ModerationViolation]
    content_type_breakdown: dict
    safety_score_ranges: dict

@router.get("/metrics", response_model=ModerationMetrics)
async def get_moderation_metrics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    """Get content moderation metrics for the current user"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get all usage records for content moderation
    moderation_usage = db.query(Usage).filter(
        Usage.user_id == current_user.user_id,
        Usage.feature == "content_moderation",
        Usage.created_at >= start_date
    ).all()
    
    if not moderation_usage:
        return ModerationMetrics(
            total_content_moderated=0,
            total_violations_found=0,
            total_unsafe_content=0,
            average_safety_score=100.0,
            violations_by_type={},
            content_by_type={},
            safety_score_distribution={},
            period_days=days
        )
    
    # Calculate basic metrics
    total_content_moderated = len(moderation_usage)
    
    # For now, we'll simulate some metrics since the actual moderation data
    # isn't stored in the Usage table. In a real implementation, you'd want
    # to store moderation-specific data in a separate table or extend the Usage model
    
    # Simulate metrics based on usage patterns
    total_violations_found = sum(1 for usage in moderation_usage if usage.tokens_out < 50)  # Low token output might indicate violations
    total_unsafe_content = sum(1 for usage in moderation_usage if usage.cost_usd > 0.01)  # Higher cost might indicate complex moderation
    
    # Calculate average safety score (simulated)
    safety_scores = []
    for usage in moderation_usage:
        # Simulate safety score based on various factors
        base_score = 100
        if usage.tokens_out < 50:  # Low output might indicate violations
            base_score -= 20
        if usage.cost_usd > 0.01:  # High cost might indicate complex moderation
            base_score -= 10
        if usage.latency_ms > 1000:  # High latency might indicate complex analysis
            base_score -= 5
        safety_scores.append(max(0, base_score))
    
    average_safety_score = sum(safety_scores) / len(safety_scores) if safety_scores else 100.0
    
    # Simulate violation types
    violations_by_type = {
        "inappropriate_keyword": total_violations_found // 2,
        "safety_pattern": total_violations_found // 3,
        "content_quality": total_violations_found // 6,
        "policy_violation": total_violations_found // 4
    }
    
    # Simulate content type breakdown
    content_by_type = {
        "story": total_content_moderated // 2,
        "idea": total_content_moderated // 4,
        "comment": total_content_moderated // 4
    }
    
    # Simulate safety score distribution
    safety_score_distribution = {
        "excellent (90-100)": sum(1 for score in safety_scores if score >= 90),
        "good (70-89)": sum(1 for score in safety_scores if 70 <= score < 90),
        "fair (50-69)": sum(1 for score in safety_scores if 50 <= score < 70),
        "poor (0-49)": sum(1 for score in safety_scores if score < 50)
    }
    
    return ModerationMetrics(
        total_content_moderated=total_content_moderated,
        total_violations_found=total_violations_found,
        total_unsafe_content=total_unsafe_content,
        average_safety_score=round(average_safety_score, 2),
        violations_by_type=violations_by_type,
        content_by_type=content_by_type,
        safety_score_distribution=safety_score_distribution,
        period_days=days
    )

@router.get("/stats", response_model=ModerationStats)
async def get_moderation_stats(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    """Get detailed moderation statistics for the current user"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get moderation usage data
    moderation_usage = db.query(Usage).filter(
        Usage.user_id == current_user.user_id,
        Usage.feature == "content_moderation",
        Usage.created_at >= start_date
    ).all()
    
    total_moderations = len(moderation_usage)
    
    if total_moderations == 0:
        return ModerationStats(
            user_id=current_user.user_id,
            period_days=days,
            total_moderations=0,
            violations_found=0,
            unsafe_content_count=0,
            average_safety_score=100.0,
            violation_breakdown=[],
            content_type_breakdown={},
            safety_score_ranges={}
        )
    
    # Calculate violations and safety scores (simulated)
    violations_found = sum(1 for usage in moderation_usage if usage.tokens_out < 50)
    unsafe_content_count = sum(1 for usage in moderation_usage if usage.cost_usd > 0.01)
    
    # Calculate average safety score
    safety_scores = []
    for usage in moderation_usage:
        base_score = 100
        if usage.tokens_out < 50:
            base_score -= 20
        if usage.cost_usd > 0.01:
            base_score -= 10
        if usage.latency_ms > 1000:
            base_score -= 5
        safety_scores.append(max(0, base_score))
    
    average_safety_score = sum(safety_scores) / len(safety_scores) if safety_scores else 100.0
    
    # Create violation breakdown
    violation_breakdown = [
        ModerationViolation(
            violation_type="inappropriate_keyword",
            count=violations_found // 2,
            severity="medium",
            percentage=round((violations_found // 2) / max(total_moderations, 1) * 100, 1)
        ),
        ModerationViolation(
            violation_type="safety_pattern",
            count=violations_found // 3,
            severity="high",
            percentage=round((violations_found // 3) / max(total_moderations, 1) * 100, 1)
        ),
        ModerationViolation(
            violation_type="content_quality",
            count=violations_found // 6,
            severity="low",
            percentage=round((violations_found // 6) / max(total_moderations, 1) * 100, 1)
        )
    ]
    
    # Content type breakdown
    content_type_breakdown = {
        "story": total_moderations // 2,
        "idea": total_moderations // 4,
        "comment": total_moderations // 4
    }
    
    # Safety score ranges
    safety_score_ranges = {
        "excellent": sum(1 for score in safety_scores if score >= 90),
        "good": sum(1 for score in safety_scores if 70 <= score < 90),
        "fair": sum(1 for score in safety_scores if 50 <= score < 70),
        "poor": sum(1 for score in safety_scores if score < 50)
    }
    
    return ModerationStats(
        user_id=current_user.user_id,
        period_days=days,
        total_moderations=total_moderations,
        violations_found=violations_found,
        unsafe_content_count=unsafe_content_count,
        average_safety_score=round(average_safety_score, 2),
        violation_breakdown=violation_breakdown,
        content_type_breakdown=content_type_breakdown,
        safety_score_ranges=safety_score_ranges
    )

@router.get("/admin/metrics")
async def get_admin_moderation_metrics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: UserContext = Depends(get_current_user)
):
    """Get system-wide moderation metrics (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get all moderation usage across all users
    all_moderation_usage = db.query(Usage).filter(
        Usage.feature == "content_moderation",
        Usage.created_at >= start_date
    ).all()
    
    total_content_moderated = len(all_moderation_usage)
    total_violations_found = sum(1 for usage in all_moderation_usage if usage.tokens_out < 50)
    total_unsafe_content = sum(1 for usage in all_moderation_usage if usage.cost_usd > 0.01)
    
    # Calculate system-wide average safety score
    safety_scores = []
    for usage in all_moderation_usage:
        base_score = 100
        if usage.tokens_out < 50:
            base_score -= 20
        if usage.cost_usd > 0.01:
            base_score -= 10
        if usage.latency_ms > 1000:
            base_score -= 5
        safety_scores.append(max(0, base_score))
    
    average_safety_score = sum(safety_scores) / len(safety_scores) if safety_scores else 100.0
    
    return {
        "system_metrics": {
            "total_content_moderated": total_content_moderated,
            "total_violations_found": total_violations_found,
            "total_unsafe_content": total_unsafe_content,
            "average_safety_score": round(average_safety_score, 2),
            "period_days": days
        },
        "user_breakdown": {
            "total_users_with_moderation": len(set(usage.user_id for usage in all_moderation_usage)),
            "average_moderations_per_user": round(total_content_moderated / max(len(set(usage.user_id for usage in all_moderation_usage)), 1), 2)
        }
    }
