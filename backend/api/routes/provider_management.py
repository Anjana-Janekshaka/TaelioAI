from fastapi import APIRouter, Depends, HTTPException, Query
from auth.dependencies import get_current_user, UserContext
from services.providers.router import router as provider_router
from services.providers.config import get_available_providers, PROVIDER_CHARACTERISTICS
from typing import Optional
import os

router = APIRouter()

@router.get("/providers/available")
async def get_available_providers_list(
    current_user: UserContext = Depends(get_current_user)
):
    """Get list of available providers"""
    available = provider_router.get_available_providers()
    
    # Add provider characteristics
    provider_info = {}
    for provider in available:
        characteristics = PROVIDER_CHARACTERISTICS.get(provider, {})
        provider_info[provider] = {
            "available": True,
            "characteristics": characteristics,
            "api_key_configured": True
        }
    
    # Add unavailable providers
    all_providers = ["gemini", "openai", "anthropic"]
    for provider in all_providers:
        if provider not in available:
            characteristics = PROVIDER_CHARACTERISTICS.get(provider, {})
            provider_info[provider] = {
                "available": False,
                "characteristics": characteristics,
                "api_key_configured": bool(os.getenv(f"{provider.upper()}_API_KEY"))
            }
    
    return {
        "available_providers": available,
        "provider_details": provider_info,
        "total_providers": len(all_providers)
    }

@router.get("/providers/selection-info")
async def get_provider_selection_info(
    task: str = Query(..., description="Task type: idea or story"),
    tier: str = Query("free", description="User tier: free, pro, or admin"),
    current_user: UserContext = Depends(get_current_user)
):
    """Get information about provider selection for a specific task and tier"""
    if task not in ["idea", "story"]:
        raise HTTPException(status_code=400, detail="Task must be 'idea' or 'story'")
    
    if tier not in ["free", "pro", "admin"]:
        raise HTTPException(status_code=400, detail="Tier must be 'free', 'pro', or 'admin'")
    
    info = provider_router.get_provider_info(task, tier)
    
    # Add model information
    from services.providers.config import get_model_for_provider, TaskType, TierType, ProviderType
    
    task_enum = TaskType(task)
    tier_enum = TierType(tier)
    
    models = {}
    for provider_name in info["available_providers"]:
        try:
            provider_enum = ProviderType(provider_name)
            model = get_model_for_provider(task_enum, tier_enum, provider_enum)
            models[provider_name] = model
        except ValueError:
            models[provider_name] = None
    
    info["models"] = models
    
    return info

@router.post("/providers/test")
async def test_provider(
    provider: str = Query(..., description="Provider to test: gemini, openai, or anthropic"),
    task: str = Query("idea", description="Task type: idea or story"),
    current_user: UserContext = Depends(get_current_user)
):
    """Test a specific provider"""
    if current_user.tier not in ["admin", "pro"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if provider not in ["gemini", "openai", "anthropic"]:
        raise HTTPException(status_code=400, detail="Invalid provider")
    
    if task not in ["idea", "story"]:
        raise HTTPException(status_code=400, detail="Task must be 'idea' or 'story'")
    
    try:
        # Create a test provider
        test_provider = provider_router._create_provider(
            provider, task, current_user.tier
        )
        
        # Test with simple input
        if task == "idea":
            from schemas.idea import IdeaRequest
            test_request = IdeaRequest(
                prompt="Test prompt for provider testing",
                genre="Test",
                tone="Neutral"
            )
            result = test_provider.generate(test_request)
        else:  # story
            from schemas.story import StoryRequest
            test_request = StoryRequest(
                title="Test Story",
                genre="Test",
                outline="A simple test story outline"
            )
            result = test_provider.generate(test_request)
        
        return {
            "provider": provider,
            "task": task,
            "success": True,
            "test_result": {
                "provider": result.provider,
                "model": result.model,
                "tokens_in": result.tokens_in,
                "tokens_out": result.tokens_out,
                "latency_ms": result.latency_ms,
                "cost_usd": result.cost_usd
            }
        }
        
    except Exception as e:
        return {
            "provider": provider,
            "task": task,
            "success": False,
            "error": str(e)
        }

@router.get("/providers/health")
async def get_providers_health(
    current_user: UserContext = Depends(get_current_user)
):
    """Get health status of all providers"""
    if current_user.tier not in ["admin", "pro"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    health_status = {}
    available_providers = provider_router.get_available_providers()
    
    for provider in ["gemini", "openai", "anthropic"]:
        try:
            if provider in available_providers:
                # Quick test
                test_provider = provider_router._create_provider(provider, "idea", "free")
                health_status[provider] = {
                    "status": "healthy",
                    "available": True,
                    "api_key_configured": True
                }
            else:
                health_status[provider] = {
                    "status": "unavailable",
                    "available": False,
                    "api_key_configured": bool(os.getenv(f"{provider.upper()}_API_KEY")),
                    "reason": "API key not configured"
                }
        except Exception as e:
            health_status[provider] = {
                "status": "error",
                "available": False,
                "api_key_configured": bool(os.getenv(f"{provider.upper()}_API_KEY")),
                "error": str(e)
            }
    
    return {
        "providers_health": health_status,
        "overall_status": "healthy" if all(p["status"] == "healthy" for p in health_status.values()) else "degraded"
    }
