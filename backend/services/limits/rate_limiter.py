import time
import redis
import os
from fastapi import HTTPException
from typing import Dict, Tuple
import json
from sqlalchemy.orm import Session
from db.database import SessionLocal
from services.usage_tracker import UsageTracker

# Redis connection (optional)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    REDIS_AVAILABLE = True
except:
    redis_client = None
    REDIS_AVAILABLE = False

class RatePolicy:
    def __init__(self, capacity: int, refill_per_sec: float):
        self.capacity = capacity
        self.refill_per_sec = refill_per_sec

# Tier-based policies
FREE_POLICY = RatePolicy(capacity=2, refill_per_sec=2/60)   # ~2 per minute
PRO_POLICY = RatePolicy(capacity=10, refill_per_sec=10/60)  # ~10 per minute
ADMIN_POLICY = RatePolicy(capacity=100, refill_per_sec=100/60)  # ~100 per minute

def _policy_for_tier(tier: str) -> RatePolicy:
    if tier == "admin":
        return ADMIN_POLICY
    elif tier == "pro":
        return PRO_POLICY
    return FREE_POLICY

def allow(user_id: str, tier: str, route_key: str):
    """Database-backed rate limiting with usage tracking"""
    db = SessionLocal()
    try:
        # Use the usage tracker for rate limiting
        tracker = UsageTracker(db)
        limit_check = tracker.check_limits(user_id, route_key, "unknown", 0, 0)
        
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
                    "remaining": remaining,
                    "retry_after": 3600
                },
                headers={
                    "X-RateLimit-Limit": str(limit_check["limits"].get("requests_per_day", 50)),
                    "X-RateLimit-Remaining": str(remaining["requests_today"]),
                    "Retry-After": "3600"
                }
            )
        
        # If Redis is available, also use it for additional rate limiting
        if REDIS_AVAILABLE:
            _allow_redis(user_id, tier, route_key)
        else:
            _allow_in_memory(user_id, tier, route_key)
            
    finally:
        db.close()

def _allow_redis(user_id: str, tier: str, route_key: str):
    """Redis-backed rate limiting with token bucket algorithm"""
    try:
        policy = _policy_for_tier(tier)
        bucket_key = f"rate_limit:{user_id}:{route_key}"
        
        # Get current bucket state
        bucket_data = redis_client.get(bucket_key)
        now = time.time()
        
        if bucket_data:
            data = json.loads(bucket_data)
            tokens = data["tokens"]
            last_refill = data["last_refill"]
        else:
            tokens = policy.capacity
            last_refill = now
        
        # Refill tokens based on elapsed time
        elapsed = now - last_refill
        tokens = min(policy.capacity, tokens + elapsed * policy.refill_per_sec)
        
        # Check if request is allowed
        if tokens < 1.0:
            raise HTTPException(
                status_code=429, 
                detail="Rate limit exceeded",
                headers={"Retry-After": str(int(60 / policy.refill_per_sec))}
            )
        
        # Consume token
        tokens -= 1.0
        
        # Update bucket state
        bucket_data = {
            "tokens": tokens,
            "last_refill": now
        }
        redis_client.setex(bucket_key, 3600, json.dumps(bucket_data))  # 1 hour TTL
        
    except redis.RedisError:
        # Fallback to in-memory if Redis is unavailable
        print("Warning: Redis unavailable, falling back to in-memory rate limiting")
        _allow_in_memory(user_id, tier, route_key)

# Fallback in-memory rate limiting
_memory_buckets: Dict[Tuple[str, str], Tuple[float, float]] = {}

def _allow_in_memory(user_id: str, tier: str, route_key: str):
    """Fallback in-memory rate limiting"""
    now = time.time()
    key = (user_id, route_key)
    policy = _policy_for_tier(tier)

    tokens, last = _memory_buckets.get(key, (policy.capacity, now))
    elapsed = now - last
    tokens = min(policy.capacity, tokens + elapsed * policy.refill_per_sec)

    if tokens < 1.0:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    tokens -= 1.0
    _memory_buckets[key] = (tokens, now)
