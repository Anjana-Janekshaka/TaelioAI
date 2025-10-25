"""
Rate limiting decorators for API endpoints
"""

from functools import wraps
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from db.database import SessionLocal
from services.usage_tracker import UsageTracker
from typing import Dict, Any
import time

def rate_limit_by_tier(tier: str = "free"):
    """
    Decorator to apply rate limiting based on user tier
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from kwargs
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                return await func(*args, **kwargs)
            
            # Get user ID from request
            user_id = get_user_id_from_request(request)
            if not user_id:
                return await func(*args, **kwargs)
            
            # Check rate limits
            db = SessionLocal()
            try:
                tracker = UsageTracker(db)
                limit_check = tracker.check_limits(user_id, "api_call", "unknown", 0, 0)
                
                if not limit_check["can_proceed"]:
                    exceeded_limits = limit_check["exceeded_limits"]
                    remaining = limit_check["remaining"]
                    
                    error_message = "Rate limit exceeded"
                    if "daily_requests" in exceeded_limits:
                        error_message += f" - Daily request limit reached. Remaining: {remaining['requests_today']}"
                    if "minute_requests" in exceeded_limits:
                        error_message += f" - Minute request limit reached. Remaining: {remaining['requests_minute']}"
                    if "daily_tokens" in exceeded_limits:
                        error_message += f" - Daily token limit reached. Remaining: {remaining['tokens_today']}"
                    
                    raise HTTPException(
                        status_code=429,
                        detail={
                            "message": error_message,
                            "rate_limit_exceeded": True,
                            "exceeded_limits": exceeded_limits,
                            "remaining": remaining
                        }
                    )
                
                # Proceed with the request
                return await func(*args, **kwargs)
            finally:
                db.close()
        
        return wrapper
    return decorator

def rate_limit_requests(requests_per_minute: int = 10, requests_per_day: int = 100):
    """
    Decorator to apply specific rate limits to an endpoint
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # This would implement endpoint-specific rate limiting
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def get_user_id_from_request(request: Request) -> str:
    """Extract user ID from request"""
    # Try to get from Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        # In a real implementation, you'd decode the JWT token here
        # For now, we'll use a simple approach
        return "user_from_token"
    
    # Try to get from X-User-ID header (for testing)
    return request.headers.get("X-User-ID")

# Tier-based rate limit configurations
TIER_RATE_LIMITS = {
    "free": {
        "requests_per_minute": 2,
        "requests_per_day": 50,
        "tokens_per_day": 10000
    },
    "pro": {
        "requests_per_minute": 10,
        "requests_per_day": 500,
        "tokens_per_day": 100000
    },
    "admin": {
        "requests_per_minute": 100,
        "requests_per_day": 10000,
        "tokens_per_day": 1000000
    }
}

def get_tier_rate_limits(tier: str) -> Dict[str, int]:
    """Get rate limits for a specific tier"""
    return TIER_RATE_LIMITS.get(tier, TIER_RATE_LIMITS["free"])

# Rate limit response helper
def create_rate_limit_response(exceeded_limits: list, remaining: dict, limits: dict) -> dict:
    """Create a standardized rate limit response"""
    return {
        "detail": "Rate limit exceeded",
        "rate_limit_exceeded": True,
        "exceeded_limits": exceeded_limits,
        "remaining": remaining,
        "limits": limits,
        "retry_after": 3600  # Retry after 1 hour
    }
