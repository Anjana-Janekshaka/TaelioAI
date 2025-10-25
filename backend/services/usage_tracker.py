"""
Usage tracking service that monitors and enforces tier limits
"""

from sqlalchemy.orm import Session
from db.models import Usage, Plan, User
from datetime import datetime, timedelta
import json
from typing import Dict, Any, Optional

class UsageTracker:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_limits(self, user_id: str) -> Dict[str, Any]:
        """Get user's tier limits"""
        plan = self.db.query(Plan).filter(Plan.user_id == user_id).first()
        if not plan:
            return {"requests_per_day": 50, "requests_per_minute": 2, "tokens_per_day": 10000}
        
        try:
            limits = json.loads(plan.limits_json) if plan.limits_json else {}
        except json.JSONDecodeError:
            limits = {"requests_per_day": 50, "requests_per_minute": 2, "tokens_per_day": 10000}
        
        return limits
    
    def check_limits(self, user_id: str, feature: str, provider: str, tokens_in: int = 0, tokens_out: int = 0) -> Dict[str, Any]:
        """Check if user has exceeded their limits"""
        limits = self.get_user_limits(user_id)
        
        # Get current usage for today
        today = datetime.utcnow().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        
        # Count requests today
        requests_today = self.db.query(Usage).filter(
            Usage.user_id == user_id,
            Usage.created_at >= start_of_day
        ).count()
        
        # Count requests in last minute
        one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
        requests_last_minute = self.db.query(Usage).filter(
            Usage.user_id == user_id,
            Usage.created_at >= one_minute_ago
        ).count()
        
        # Calculate total tokens used today
        usage_today = self.db.query(Usage).filter(
            Usage.user_id == user_id,
            Usage.created_at >= start_of_day
        ).all()
        
        total_tokens_today = sum(usage.tokens_in + usage.tokens_out for usage in usage_today)
        
        # Check limits
        exceeded_limits = []
        
        if requests_today >= limits.get("requests_per_day", 50):
            exceeded_limits.append("daily_requests")
        
        if requests_last_minute >= limits.get("requests_per_minute", 2):
            exceeded_limits.append("minute_requests")
        
        if total_tokens_today + tokens_in + tokens_out > limits.get("tokens_per_day", 10000):
            exceeded_limits.append("daily_tokens")
        
        return {
            "can_proceed": len(exceeded_limits) == 0,
            "exceeded_limits": exceeded_limits,
            "current_usage": {
                "requests_today": requests_today,
                "requests_last_minute": requests_last_minute,
                "tokens_today": total_tokens_today,
                "tokens_this_request": tokens_in + tokens_out
            },
            "limits": limits,
            "remaining": {
                "requests_today": max(0, limits.get("requests_per_day", 50) - requests_today),
                "requests_minute": max(0, limits.get("requests_per_minute", 2) - requests_last_minute),
                "tokens_today": max(0, limits.get("tokens_per_day", 10000) - total_tokens_today)
            }
        }
    
    def log_usage(self, user_id: str, feature: str, provider: str, model: str, 
                  tokens_in: int, tokens_out: int, latency_ms: int, cost_usd: float) -> Usage:
        """Log usage to database"""
        usage = Usage(
            user_id=user_id,
            feature=feature,
            provider=provider,
            model=model,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            latency_ms=latency_ms,
            cost_usd=cost_usd
        )
        
        self.db.add(usage)
        self.db.commit()
        
        return usage
    
    def get_usage_summary(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get user's usage summary for the specified period"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all usage records for the period
        usage_records = self.db.query(Usage).filter(
            Usage.user_id == user_id,
            Usage.created_at >= start_date
        ).all()
        
        if not usage_records:
            return {
                "total_requests": 0,
                "total_tokens_in": 0,
                "total_tokens_out": 0,
                "total_cost": 0.0,
                "feature_breakdown": {},
                "provider_breakdown": {},
                "daily_usage": []
            }
        
        # Calculate totals
        total_requests = len(usage_records)
        total_tokens_in = sum(record.tokens_in for record in usage_records)
        total_tokens_out = sum(record.tokens_out for record in usage_records)
        total_cost = sum(record.cost_usd for record in usage_records)
        
        # Feature breakdown
        feature_breakdown = {}
        for record in usage_records:
            if record.feature not in feature_breakdown:
                feature_breakdown[record.feature] = {"requests": 0, "tokens": 0, "cost": 0.0}
            feature_breakdown[record.feature]["requests"] += 1
            feature_breakdown[record.feature]["tokens"] += record.tokens_in + record.tokens_out
            feature_breakdown[record.feature]["cost"] += record.cost_usd
        
        # Provider breakdown
        provider_breakdown = {}
        for record in usage_records:
            if record.provider not in provider_breakdown:
                provider_breakdown[record.provider] = {"requests": 0, "tokens": 0, "cost": 0.0}
            provider_breakdown[record.provider]["requests"] += 1
            provider_breakdown[record.provider]["tokens"] += record.tokens_in + record.tokens_out
            provider_breakdown[record.provider]["cost"] += record.cost_usd
        
        # Daily usage (last 7 days)
        daily_usage = []
        for i in range(7):
            date = (datetime.utcnow() - timedelta(days=i)).date()
            day_start = datetime.combine(date, datetime.min.time())
            day_end = datetime.combine(date, datetime.max.time())
            
            day_records = [r for r in usage_records if day_start <= r.created_at <= day_end]
            daily_usage.append({
                "date": date.isoformat(),
                "requests": len(day_records),
                "tokens": sum(r.tokens_in + r.tokens_out for r in day_records),
                "cost": sum(r.cost_usd for r in day_records)
            })
        
        return {
            "total_requests": total_requests,
            "total_tokens_in": total_tokens_in,
            "total_tokens_out": total_tokens_out,
            "total_cost": total_cost,
            "feature_breakdown": feature_breakdown,
            "provider_breakdown": provider_breakdown,
            "daily_usage": daily_usage
        }
    
    def get_tier_info(self, user_id: str) -> Dict[str, Any]:
        """Get user's tier information and remaining limits"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return {}
        
        plan = self.db.query(Plan).filter(Plan.user_id == user_id).first()
        if not plan:
            return {"tier": "free", "role": user.role}
        
        limits = self.get_user_limits(user_id)
        current_usage = self.check_limits(user_id, "", "", 0, 0)
        
        return {
            "tier": plan.tier,
            "role": user.role,
            "limits": limits,
            "current_usage": current_usage["current_usage"],
            "remaining": {
                "requests_today": max(0, limits.get("requests_per_day", 50) - current_usage["current_usage"]["requests_today"]),
                "tokens_today": max(0, limits.get("tokens_per_day", 10000) - current_usage["current_usage"]["tokens_today"])
            }
        }
