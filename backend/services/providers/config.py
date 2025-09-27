"""
Provider configuration and routing logic
"""
from typing import Dict, List, Optional
from enum import Enum

class ProviderType(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class TaskType(Enum):
    IDEA = "idea"
    STORY = "story"

class TierType(Enum):
    FREE = "free"
    PRO = "pro"
    ADMIN = "admin"

# Provider availability configuration
PROVIDER_AVAILABILITY = {
    ProviderType.GEMINI: {
        "available": True,
        "api_key_env": "GEMINI_API_KEY",
        "fallback_priority": 3
    },
    ProviderType.OPENAI: {
        "available": True,
        "api_key_env": "OPENAI_API_KEY", 
        "fallback_priority": 1
    },
    ProviderType.ANTHROPIC: {
        "available": True,
        "api_key_env": "ANTHROPIC_API_KEY",
        "fallback_priority": 2
    }
}

# Model selection by tier and task
MODEL_CONFIGURATIONS = {
    TaskType.IDEA: {
        TierType.FREE: {
            "primary": ProviderType.GEMINI,
            "models": {
                ProviderType.GEMINI: "gemini-1.5-flash",
                ProviderType.OPENAI: "gpt-3.5-turbo",
                ProviderType.ANTHROPIC: "claude-3-haiku-20240307"
            },
            "fallback_order": [ProviderType.GEMINI, ProviderType.OPENAI, ProviderType.ANTHROPIC]
        },
        TierType.PRO: {
            "primary": ProviderType.OPENAI,
            "models": {
                ProviderType.OPENAI: "gpt-4",
                ProviderType.ANTHROPIC: "claude-3-sonnet-20240229",
                ProviderType.GEMINI: "gemini-1.5-pro"
            },
            "fallback_order": [ProviderType.OPENAI, ProviderType.ANTHROPIC, ProviderType.GEMINI]
        },
        TierType.ADMIN: {
            "primary": ProviderType.ANTHROPIC,
            "models": {
                ProviderType.ANTHROPIC: "claude-3-sonnet-20240229",
                ProviderType.OPENAI: "gpt-4",
                ProviderType.GEMINI: "gemini-1.5-pro"
            },
            "fallback_order": [ProviderType.ANTHROPIC, ProviderType.OPENAI, ProviderType.GEMINI]
        }
    },
    TaskType.STORY: {
        TierType.FREE: {
            "primary": ProviderType.GEMINI,
            "models": {
                ProviderType.GEMINI: "gemini-1.5-flash",
                ProviderType.OPENAI: "gpt-3.5-turbo",
                ProviderType.ANTHROPIC: "claude-3-haiku-20240307"
            },
            "fallback_order": [ProviderType.GEMINI, ProviderType.OPENAI, ProviderType.ANTHROPIC]
        },
        TierType.PRO: {
            "primary": ProviderType.ANTHROPIC,
            "models": {
                ProviderType.ANTHROPIC: "claude-3-sonnet-20240229",
                ProviderType.OPENAI: "gpt-4",
                ProviderType.GEMINI: "gemini-1.5-pro"
            },
            "fallback_order": [ProviderType.ANTHROPIC, ProviderType.OPENAI, ProviderType.GEMINI]
        },
        TierType.ADMIN: {
            "primary": ProviderType.OPENAI,
            "models": {
                ProviderType.OPENAI: "gpt-4",
                ProviderType.ANTHROPIC: "claude-3-sonnet-20240229",
                ProviderType.GEMINI: "gemini-1.5-pro"
            },
            "fallback_order": [ProviderType.OPENAI, ProviderType.ANTHROPIC, ProviderType.GEMINI]
        }
    }
}

# Performance and cost considerations
PROVIDER_CHARACTERISTICS = {
    ProviderType.GEMINI: {
        "speed": "fast",
        "cost": "low",
        "quality": "good",
        "reliability": "high"
    },
    ProviderType.OPENAI: {
        "speed": "medium",
        "cost": "high",
        "quality": "excellent",
        "reliability": "high"
    },
    ProviderType.ANTHROPIC: {
        "speed": "medium",
        "cost": "medium",
        "quality": "excellent",
        "reliability": "high"
    }
}

def get_provider_config(task: TaskType, tier: TierType) -> Dict:
    """Get provider configuration for a specific task and tier"""
    return MODEL_CONFIGURATIONS.get(task, {}).get(tier, {})

def get_available_providers() -> List[ProviderType]:
    """Get list of available providers based on API key availability"""
    import os
    available = []
    
    for provider, config in PROVIDER_AVAILABILITY.items():
        if config["available"] and os.getenv(config["api_key_env"]):
            available.append(provider)
    
    return available

def get_fallback_providers(task: TaskType, tier: TierType) -> List[ProviderType]:
    """Get fallback provider order for a specific task and tier"""
    config = get_provider_config(task, tier)
    fallback_order = config.get("fallback_order", [])
    
    # Filter to only available providers
    available_providers = get_available_providers()
    return [p for p in fallback_order if p in available_providers]

def get_primary_provider(task: TaskType, tier: TierType) -> Optional[ProviderType]:
    """Get primary provider for a specific task and tier"""
    config = get_provider_config(task, tier)
    primary = config.get("primary")
    
    # Check if primary provider is available
    if primary and primary in get_available_providers():
        return primary
    
    # Return first available fallback
    fallbacks = get_fallback_providers(task, tier)
    return fallbacks[0] if fallbacks else None

def get_model_for_provider(task: TaskType, tier: TierType, provider: ProviderType) -> Optional[str]:
    """Get specific model for a provider, task, and tier"""
    config = get_provider_config(task, tier)
    models = config.get("models", {})
    return models.get(provider)
