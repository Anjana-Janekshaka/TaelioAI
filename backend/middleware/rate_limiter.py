"""
Rate limiting middleware for API endpoints
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.orm import Session
from db.database import SessionLocal
from services.usage_tracker import UsageTracker
from typing import Dict, Any
import time
import json

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_cache: Dict[str, Dict[str, Any]] = {}
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for certain paths
        if self._should_skip_rate_limit(request):
            return await call_next(request)
        
        # Get user info from request
        user_id = self._get_user_id(request)
        if not user_id:
            return await call_next(request)
        
        # Check rate limits
        rate_limit_result = self._check_rate_limits(user_id, request)
        
        if not rate_limit_result["allowed"]:
            return self._create_rate_limit_response(rate_limit_result)
        
        # Add rate limit headers to response
        response = await call_next(request)
        self._add_rate_limit_headers(response, rate_limit_result)
        
        return response
    
    def _should_skip_rate_limit(self, request: Request) -> bool:
        """Skip rate limiting for certain paths"""
        skip_paths = [
            "/docs",
            "/redoc", 
            "/openapi.json",
            "/health",
            "/metrics",
            "/favicon.ico"
        ]
        
        return any(request.url.path.startswith(path) for path in skip_paths)
    
    def _get_user_id(self, request: Request) -> str:
        """Extract user ID from request headers or JWT token"""
        # Try to get from Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # In a real implementation, you'd decode the JWT token here
            # For now, we'll use a simple approach
            return "user_from_token"
        
        # Try to get from X-User-ID header (for testing)
        return request.headers.get("X-User-ID")
    
    def _check_rate_limits(self, user_id: str, request: Request) -> Dict[str, Any]:
        """Check if user has exceeded rate limits"""
        db = SessionLocal()
        try:
            tracker = UsageTracker(db)
            
            # Get user's tier limits
            tier_info = tracker.get_tier_info(user_id)
            limits = tier_info.get("limits", {})
            current_usage = tier_info.get("current_usage", {})
            
            # Check daily limits
            daily_requests = current_usage.get("requests_today", 0)
            daily_limit = limits.get("requests_per_day", 50)
            
            # Check minute limits
            minute_requests = current_usage.get("requests_last_minute", 0)
            minute_limit = limits.get("requests_per_minute", 2)
            
            # Check token limits
            daily_tokens = current_usage.get("tokens_today", 0)
            token_limit = limits.get("tokens_per_day", 10000)
            
            # Determine if limits are exceeded
            exceeded_limits = []
            if daily_requests >= daily_limit:
                exceeded_limits.append("daily_requests")
            if minute_requests >= minute_limit:
                exceeded_limits.append("minute_requests")
            if daily_tokens >= token_limit:
                exceeded_limits.append("daily_tokens")
            
            return {
                "allowed": len(exceeded_limits) == 0,
                "exceeded_limits": exceeded_limits,
                "limits": limits,
                "current_usage": current_usage,
                "remaining": {
                    "requests_today": max(0, daily_limit - daily_requests),
                    "requests_minute": max(0, minute_limit - minute_requests),
                    "tokens_today": max(0, token_limit - daily_tokens)
                },
                "reset_time": {
                    "daily": self._get_daily_reset_time(),
                    "minute": self._get_minute_reset_time()
                }
            }
        finally:
            db.close()
    
    def _create_rate_limit_response(self, rate_limit_result: Dict[str, Any]) -> Response:
        """Create rate limit exceeded response"""
        exceeded_limits = rate_limit_result["exceeded_limits"]
        remaining = rate_limit_result["remaining"]
        
        error_message = "Rate limit exceeded"
        if "daily_requests" in exceeded_limits:
            error_message += f" - Daily request limit reached. Remaining: {remaining['requests_today']}"
        if "minute_requests" in exceeded_limits:
            error_message += f" - Minute request limit reached. Remaining: {remaining['requests_minute']}"
        if "daily_tokens" in exceeded_limits:
            error_message += f" - Daily token limit reached. Remaining: {remaining['tokens_today']}"
        
        return Response(
            content=json.dumps({
                "detail": error_message,
                "rate_limit_exceeded": True,
                "exceeded_limits": exceeded_limits,
                "remaining": remaining,
                "reset_times": rate_limit_result["reset_time"]
            }),
            status_code=429,
            media_type="application/json",
            headers={
                "X-RateLimit-Limit": str(rate_limit_result["limits"].get("requests_per_day", 50)),
                "X-RateLimit-Remaining": str(remaining["requests_today"]),
                "X-RateLimit-Reset": str(int(rate_limit_result["reset_time"]["daily"])),
                "Retry-After": str(3600)  # Retry after 1 hour
            }
        )
    
    def _add_rate_limit_headers(self, response: Response, rate_limit_result: Dict[str, Any]):
        """Add rate limit headers to response"""
        limits = rate_limit_result["limits"]
        remaining = rate_limit_result["remaining"]
        
        response.headers["X-RateLimit-Limit"] = str(limits.get("requests_per_day", 50))
        response.headers["X-RateLimit-Remaining"] = str(remaining["requests_today"])
        response.headers["X-RateLimit-Reset"] = str(int(rate_limit_result["reset_time"]["daily"]))
        response.headers["X-RateLimit-Tier"] = "free"  # This would come from user tier
    
    def _get_daily_reset_time(self) -> float:
        """Get timestamp for daily reset (midnight)"""
        import datetime
        now = datetime.datetime.now()
        tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        return tomorrow.timestamp()
    
    def _get_minute_reset_time(self) -> float:
        """Get timestamp for minute reset"""
        return time.time() + 60

# Rate limit decorator for individual endpoints
def rate_limit(requests_per_minute: int = 10, requests_per_day: int = 100):
    """Decorator to apply rate limiting to specific endpoints"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This would be implemented per endpoint
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Tier-based rate limits
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
