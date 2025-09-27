import time
import redis
import os
from fastapi import HTTPException
from typing import Dict, Tuple
import json

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

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
