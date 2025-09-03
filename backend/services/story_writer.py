import os
import google.generativeai as genai
from schemas.story import StoryRequest, StoryResponse

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_story(request: StoryRequest) -> StoryResponse:
    model = genai.GenerativeModel("gemini-pro")  

    prompt = f"""
    You are a professional story writer.
    Title: {request.title}
    Genre: {request.genre}
    Outline: {request.outline}

    Write a detailed story with proper structure:
    - Introduction
    - Character development
    - Conflict
    - Resolution
    """

    response = model.generate_content(prompt)

    story_text = response.text if hasattr(response, "text") else str(response)
    return StoryResponse(story=story_text.strip())
