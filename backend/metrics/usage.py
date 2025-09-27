import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from db.database import get_db
from db.models import Usage
from sqlalchemy.orm import Session
from typing import Optional
from .prom import record_request_metrics, record_usage_metrics

class UsageLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        request_id = str(uuid.uuid4())
        
        # Store request ID for later use
        request.state.request_id = request_id
        
        response = await call_next(request)
        
        elapsed_ms = int((time.time() - start) * 1000)
        elapsed_seconds = elapsed_ms / 1000.0  # Convert to seconds for Prometheus
        path = request.url.path
        method = request.method
        status_code = response.status_code
        
        # Extract user tier from request state (set by auth middleware)
        user_tier = getattr(request.state, 'user_tier', 'unknown')
        
        # Record Prometheus metrics
        try:
            record_request_metrics(
                method=method,
                endpoint=path,
                status_code=status_code,
                user_tier=user_tier,
                duration=elapsed_seconds
            )
        except Exception as e:
            print(f"Failed to record Prometheus metrics: {e}")
        
        # Log to console
        print(f"USAGE request_id={request_id} path={path} method={method} latency_ms={elapsed_ms} user_tier={user_tier}")
        
        return response

def log_usage(
    user_id: str,
    feature: str,
    provider: str,
    model: str,
    tokens_in: int,
    tokens_out: int,
    latency_ms: int,
    cost_usd: float,
    db: Session,
    user_tier: str = "unknown"
):
    """Log usage to database and Prometheus metrics"""
    try:
        # Log to database
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
        db.add(usage)
        db.commit()
        
        # Record Prometheus metrics
        try:
            record_usage_metrics(
                provider=provider,
                model=model,
                feature=feature,
                user_tier=user_tier,
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                cost_usd=cost_usd
            )
        except Exception as e:
            print(f"Failed to record Prometheus usage metrics: {e}")
            
    except Exception as e:
        print(f"Failed to log usage: {e}")
        db.rollback()

def get_user_usage_summary(user_id: str, days: int = 30, db: Session = None) -> dict:
    """Get usage summary for a user"""
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get total usage
    total_usage = db.query(Usage).filter(
        Usage.user_id == user_id,
        Usage.created_at >= start_date
    ).all()
    
    # Aggregate by feature
    feature_stats = {}
    total_tokens_in = 0
    total_tokens_out = 0
    total_cost = 0.0
    total_requests = len(total_usage)
    
    for usage in total_usage:
        feature = usage.feature
        if feature not in feature_stats:
            feature_stats[feature] = {
                "requests": 0,
                "tokens_in": 0,
                "tokens_out": 0,
                "cost": 0.0,
                "avg_latency": 0
            }
        
        feature_stats[feature]["requests"] += 1
        feature_stats[feature]["tokens_in"] += usage.tokens_in
        feature_stats[feature]["tokens_out"] += usage.tokens_out
        feature_stats[feature]["cost"] += usage.cost_usd
        
        total_tokens_in += usage.tokens_in
        total_tokens_out += usage.tokens_out
        total_cost += usage.cost_usd
    
    # Calculate average latency per feature
    for feature, stats in feature_stats.items():
        if stats["requests"] > 0:
            feature_usages = [u for u in total_usage if u.feature == feature]
            avg_latency = sum(u.latency_ms for u in feature_usages) / len(feature_usages)
            stats["avg_latency"] = round(avg_latency, 2)
    
    return {
        "user_id": user_id,
        "period_days": days,
        "total_requests": total_requests,
        "total_tokens_in": total_tokens_in,
        "total_tokens_out": total_tokens_out,
        "total_cost": round(total_cost, 4),
        "feature_breakdown": feature_stats
    }
