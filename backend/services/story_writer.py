import os
import google.generativeai as genai
from schemas.story import StoryRequest, StoryResponse

def generate_story(request: StoryRequest) -> StoryResponse:
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
        # Use the most basic and widely available model
        model_names = ["gemini-pro"]
        
        model = None
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"✅ Using model: {model_name}")
                break
            except Exception as e:
                print(f"⚠️ Model {model_name} not available: {e}")
                continue
        
        if not model:
            # Try to list available models for debugging
            try:
                models = genai.list_models()
                available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
                print(f"Available models: {available_models}")
                # Try the first available model
                if available_models:
                    first_model = available_models[0].split('/')[-1]  # Get just the model name
                    print(f"Trying first available model: {first_model}")
                    model = genai.GenerativeModel(first_model)
            except Exception as list_error:
                print(f"Could not list models: {list_error}")
            
            if not model:
                raise Exception("No available Gemini model found. Please check your API access.")  

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

        # Better error handling for Gemini API response
        if response and hasattr(response, 'text'):
            story_text = response.text
        elif response and hasattr(response, 'parts'):
            # Handle case where response has parts instead of text
            story_text = ''.join([part.text for part in response.parts if hasattr(part, 'text')])
        else:
            story_text = str(response)
        
        if not story_text or story_text.strip() == "":
            raise Exception("Generated story is empty")
            
        return StoryResponse(story=story_text.strip())
    except Exception as e:
        # Log the specific error for debugging
        print(f"Error in generate_story: {str(e)}")
        raise Exception(f"Error generating story: {str(e)}")
