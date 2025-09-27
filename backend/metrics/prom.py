from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time

# Custom metrics
REQUEST_COUNT = Counter(
    'taelio_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status_code', 'user_tier']
)

REQUEST_DURATION = Histogram(
    'taelio_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint', 'user_tier']
)

TOKENS_IN = Counter(
    'taelio_tokens_in_total',
    'Total input tokens processed',
    ['provider', 'model', 'feature', 'user_tier']
)

TOKENS_OUT = Counter(
    'taelio_tokens_out_total',
    'Total output tokens generated',
    ['provider', 'model', 'feature', 'user_tier']
)

COST_USD = Counter(
    'taelio_cost_usd_total',
    'Total cost in USD',
    ['provider', 'model', 'feature', 'user_tier']
)

ACTIVE_USERS = Gauge(
    'taelio_active_users',
    'Number of active users',
    ['tier']
)

def record_request_metrics(method: str, endpoint: str, status_code: int, user_tier: str, duration: float):
    """Record request metrics"""
    REQUEST_COUNT.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code,
        user_tier=user_tier
    ).inc()
    
    REQUEST_DURATION.labels(
        method=method,
        endpoint=endpoint,
        user_tier=user_tier
    ).observe(duration)

def record_usage_metrics(provider: str, model: str, feature: str, user_tier: str, 
                        tokens_in: int, tokens_out: int, cost_usd: float):
    """Record usage metrics"""
    TOKENS_IN.labels(
        provider=provider,
        model=model,
        feature=feature,
        user_tier=user_tier
    ).inc(tokens_in)
    
    TOKENS_OUT.labels(
        provider=provider,
        model=model,
        feature=feature,
        user_tier=user_tier
    ).inc(tokens_out)
    
    COST_USD.labels(
        provider=provider,
        model=model,
        feature=feature,
        user_tier=user_tier
    ).inc(cost_usd)

def update_active_users(tier: str, count: int):
    """Update active users gauge"""
    ACTIVE_USERS.labels(tier=tier).set(count)

def get_metrics():
    """Get Prometheus metrics"""
    return generate_latest()

def create_metrics_response():
    """Create FastAPI response with metrics"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
