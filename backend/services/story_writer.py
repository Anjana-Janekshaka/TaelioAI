import os
from schemas.story import StoryRequest, StoryResponse
from services.providers.router import router

# Import Google Generative AI only when needed
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

def generate_story(request: StoryRequest, tier: str = "free") -> StoryResponse:
    # Check if Gemini is available
    if not GEMINI_AVAILABLE:
        raise ValueError("Google Generative AI is not available. Please install google-generativeai package.")
    
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
