# backend/services/story_editor.py
import os
from dotenv import load_dotenv
from google import genai  # Google Gemini SDK

### Load environment variables from backend root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def edit_story_with_gemini(story: str) -> str:
    """
    Edit story text using Google Gemini API.
    """
    try:
        prompt = f"Fix grammar, spelling, and improve style of this story:\n\n{story}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Recommended Gemini model
            contents=prompt,
        )
        return response.text

    except Exception as e:
        return f"Error editing story: {str(e)}"
