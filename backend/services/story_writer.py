import os
import google.generativeai as genai
from schemas.story import StoryRequest, StoryResponse
from services.providers.router import router
import asyncio
from typing import AsyncGenerator, Dict, Any

def generate_story(request: StoryRequest, tier: str = "free") -> StoryResponse:
    # Configure Gemini (moved here to avoid import-time errors)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set. "
            "Please create a .env file in the backend directory with: "
            "GEMINI_API_KEY=your_actual_api_key_here"
        )

    genai.configure(api_key=api_key)
    
    try:
        provider = router.select(task="story", tier=tier)
        result = provider.generate(request)
        return result.output
    except Exception as e:
        # Log the specific error for debugging
        print(f"Error in generate_story: {str(e)}")
        raise Exception(f"Error generating story: {str(e)}")

async def generate_story_streaming(request: StoryRequest, tier: str = "free", streaming_speed: str = "normal") -> AsyncGenerator[Dict[str, Any], None]:
    """Generate story with streaming support
    
    Args:
        request: Story generation request
        tier: User tier for provider selection
        streaming_speed: Speed of streaming ("slow", "normal", "fast")
    """
    # Configure streaming delays based on speed preference
    speed_config = {
        "slow": {"normal": 0.08, "punctuation": 0.2, "sentence": 0.25, "chunk_size": 10},
        "normal": {"normal": 0.05, "punctuation": 0.15, "sentence": 0.2, "chunk_size": 15},
        "fast": {"normal": 0.02, "punctuation": 0.05, "sentence": 0.08, "chunk_size": 25}
    }
    
    config = speed_config.get(streaming_speed, speed_config["normal"])
    
    try:
        provider = router.select(task="story", tier=tier)
        
        # Check if provider supports streaming
        if hasattr(provider, 'generate_streaming'):
            async for chunk in provider.generate_streaming(request):
                yield chunk
        else:
            # Fallback to regular generation with manual streaming simulation
            result = provider.generate(request)
            
            # Simulate streaming by yielding chunks of the story
            story_text = result.output.story
            chunk_size = config["chunk_size"]
            
            for i in range(0, len(story_text), chunk_size):
                chunk_text = story_text[i:i + chunk_size]
                yield {
                    'type': 'content',
                    'content': chunk_text,
                    'is_final': i + chunk_size >= len(story_text)
                }
                # Variable delay based on content - slower for punctuation, faster for regular text
                if any(p in chunk_text for p in ['.', '!', '?', '\n']):
                    await asyncio.sleep(config["sentence"])  # Longer pause for sentence endings
                elif any(p in chunk_text for p in [',', ';', ':']):
                    await asyncio.sleep(config["punctuation"])  # Medium pause for commas
                else:
                    await asyncio.sleep(config["normal"])  # Normal typing speed
            
            # Send final metadata
            yield {
                'type': 'metadata',
                'provider': result.provider,
                'model': result.model,
                'tokens_in': result.tokens_in,
                'tokens_out': result.tokens_out,
                'cost_usd': result.cost_usd
            }
            
    except Exception as e:
        yield {
            'type': 'error',
            'error': str(e)
        }
