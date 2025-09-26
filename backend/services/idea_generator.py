import os
import google.generativeai as genai
from schemas.idea import IdeaRequest, IdeaResponse
import json

def generate_idea(request: IdeaRequest) -> IdeaResponse:
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
        # Try different model names as they may have changed
        model_names = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"]
        
        model = None
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"✅ Using model for idea generation: {model_name}")
                break
            except Exception as e:
                print(f"⚠️ Model {model_name} not available: {e}")
                continue
        
        if not model:
            raise Exception("No available Gemini model found. Please check your API access.")  

        # Build the prompt for idea generation
        genre_spec = f" in the {request.genre} genre" if request.genre else ""
        tone_spec = f" with a {request.tone} tone" if request.tone else ""
        
        prompt = f"""
        You are a creative story idea generator. Based on the user's prompt, generate a compelling story idea.
        
        User Prompt: {request.prompt}
        Genre: {request.genre or 'Any genre'}
        Tone: {request.tone or 'Any tone'}
        
        Generate a story idea with the following structure:
        1. Title: A catchy, engaging title
        2. Genre: The story genre
        3. Outline: A detailed 2-3 paragraph outline of the story including:
           - Main plot points
           - Key conflicts
           - Character motivations
           - Story arc
        4. Characters: Brief description of main characters (2-3 sentences)
        5. Setting: Brief description of the story setting (1-2 sentences)
        
        Make the story idea creative, engaging, and well-structured. The outline should be detailed enough for someone to write a full story from it.
        
        Please format your response as JSON with the following structure:
        {{
            "title": "Story Title Here",
            "genre": "Genre Here",
            "outline": "Detailed outline here...",
            "characters": "Character descriptions here...",
            "setting": "Setting description here..."
        }}
        """

        response = model.generate_content(prompt)

        # Extract text from response
        if response and hasattr(response, 'text'):
            response_text = response.text
        elif response and hasattr(response, 'parts'):
            response_text = ''.join([part.text for part in response.parts if hasattr(part, 'text')])
        else:
            response_text = str(response)
        
        if not response_text or response_text.strip() == "":
            raise Exception("Generated idea is empty")
        
        # Try to parse JSON response
        try:
            # Clean up the response text to extract JSON
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            idea_data = json.loads(response_text)
            
            return IdeaResponse(
                title=idea_data.get("title", "Untitled Story"),
                genre=idea_data.get("genre", request.genre or "General"),
                outline=idea_data.get("outline", "No outline provided"),
                characters=idea_data.get("characters"),
                setting=idea_data.get("setting")
            )
            
        except json.JSONDecodeError:
            # Fallback: try to extract information from text format
            print("⚠️ JSON parsing failed, attempting text parsing...")
            return _parse_text_response(response_text, request)
            
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
