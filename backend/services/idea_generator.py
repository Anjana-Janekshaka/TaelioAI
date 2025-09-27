import os
import google.generativeai as genai
from schemas.idea import IdeaRequest, IdeaResponse
import json
from services.providers.router import router

def generate_idea(request: IdeaRequest, tier: str = "free") -> IdeaResponse:
    """
    Generate a story idea from a simple prompt using Gemini AI.
    This is the first agent in the multi-agent system.
    """
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
        provider = router.select(task="idea", tier=tier)
        result = provider.generate(request)
        return result.output
            
    except Exception as e:
        print(f"Error in generate_idea: {str(e)}")
        raise Exception(f"Error generating story idea: {str(e)}")

def _parse_text_response(text: str, request: IdeaRequest) -> IdeaResponse:
    """
    Fallback method to parse text response when JSON parsing fails.
    """
    lines = text.split('\n')
    title = "Generated Story Idea"
    genre = request.genre or "General"
    outline = text
    characters = None
    setting = None
    
    # Try to extract title from the text
    for line in lines:
        if line.strip().startswith("Title:") or line.strip().startswith("**Title:"):
            title = line.split(":", 1)[1].strip()
            break
        elif line.strip().startswith("# "):
            title = line.strip()[2:].strip()
            break
    
    # Try to extract genre
    for line in lines:
        if line.strip().startswith("Genre:") or line.strip().startswith("**Genre:"):
            genre = line.split(":", 1)[1].strip()
            break
    
    return IdeaResponse(
        title=title,
        genre=genre,
        outline=outline,
        characters=characters,
        setting=setting
    )
