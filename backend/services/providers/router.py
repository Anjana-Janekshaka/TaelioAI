from typing import Literal, Optional
from .gemini import GeminiIdeaProvider, GeminiStoryProvider
from .openai import OpenAIIdeaProvider, OpenAIStoryProvider
from .anthropic import AnthropicIdeaProvider, AnthropicStoryProvider
from .config import (
    TaskType, TierType, ProviderType, 
    get_primary_provider, get_fallback_providers, 
    get_available_providers, get_model_for_provider
)
import os

Task = Literal["idea", "story"]

class ProviderRouter:
    def __init__(self):
        self.provider_classes = {
            (ProviderType.GEMINI, "idea"): GeminiIdeaProvider,
            (ProviderType.GEMINI, "story"): GeminiStoryProvider,
            (ProviderType.OPENAI, "idea"): OpenAIIdeaProvider,
            (ProviderType.OPENAI, "story"): OpenAIStoryProvider,
            (ProviderType.ANTHROPIC, "idea"): AnthropicIdeaProvider,
            (ProviderType.ANTHROPIC, "story"): AnthropicStoryProvider,
        }
    
    def select(self, task: Task, tier: str, preferred_provider: Optional[str] = None):
        """Select the best available provider for the task and tier"""
        tier_enum = TierType(tier.lower() if tier else "free")
        task_enum = TaskType(task)
        
        # Check if preferred provider is specified and available
        if preferred_provider:
            try:
                provider_enum = ProviderType(preferred_provider.lower())
                if provider_enum in get_available_providers():
                    return self._create_provider(provider_enum, task, tier)
            except ValueError:
                pass  # Invalid provider, fall back to normal selection
        
        # Get primary provider for this task/tier combination
        primary_provider = get_primary_provider(task_enum, tier_enum)
        
        if primary_provider:
            try:
                return self._create_provider(primary_provider, task, tier)
            except Exception as e:
                print(f"⚠️ Primary provider {primary_provider} failed: {e}")
                # Fall back to other providers
        
        # Try fallback providers
        fallback_providers = get_fallback_providers(task_enum, tier_enum)
        
        for provider in fallback_providers:
            try:
                return self._create_provider(provider, task, tier)
            except Exception as e:
                print(f"⚠️ Fallback provider {provider} failed: {e}")
                continue
        
        # If all else fails, try Gemini as last resort
        try:
            print("⚠️ All configured providers failed, trying Gemini as last resort")
            return self._create_provider(ProviderType.GEMINI, task, tier)
        except Exception as e:
            raise Exception(f"All providers failed. Last error: {e}")
    
    def _create_provider(self, provider: ProviderType, task: Task, tier: str):
        """Create a provider instance"""
        provider_class = self.provider_classes.get((provider, task))
        if not provider_class:
            raise Exception(f"No provider class found for {provider} and {task}")
        
        # Check if API key is available
        api_key_env = {
            ProviderType.GEMINI: "GEMINI_API_KEY",
            ProviderType.OPENAI: "OPENAI_API_KEY",
            ProviderType.ANTHROPIC: "ANTHROPIC_API_KEY"
        }.get(provider)
        
        if not os.getenv(api_key_env):
            raise Exception(f"API key not found for {provider} (env: {api_key_env})")
        
        return provider_class(tier)
    
    def get_available_providers(self) -> list:
        """Get list of available providers"""
        available = []
        for provider in ProviderType:
            api_key_env = {
                ProviderType.GEMINI: "GEMINI_API_KEY",
                ProviderType.OPENAI: "OPENAI_API_KEY", 
                ProviderType.ANTHROPIC: "ANTHROPIC_API_KEY"
            }.get(provider)
            
            if os.getenv(api_key_env):
                available.append(provider.value)
        
        return available
    
    def get_provider_info(self, task: Task, tier: str) -> dict:
        """Get information about provider selection for debugging"""
        tier_enum = TierType(tier.lower() if tier else "free")
        task_enum = TaskType(task)
        
        primary = get_primary_provider(task_enum, tier_enum)
        fallbacks = get_fallback_providers(task_enum, tier_enum)
        available = get_available_providers()
        
        return {
            "task": task,
            "tier": tier,
            "primary_provider": primary.value if primary else None,
            "fallback_providers": [p.value for p in fallbacks],
            "available_providers": [p.value for p in available],
            "selected_provider": None  # Will be set after selection
        }

router = ProviderRouter()
