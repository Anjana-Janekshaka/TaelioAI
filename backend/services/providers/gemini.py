import time
import os
import google.generativeai as genai
from schemas.idea import IdeaRequest, IdeaResponse
from schemas.story import StoryRequest, StoryResponse
from .base import GenerationResult, IdeaProvider, StoryProvider

_DEFAULT_IDEA_MODEL = {
    "free": "gemini-2.5-flash",
    "pro": "gemini-2.5-flash"
}
_DEFAULT_STORY_MODEL = {
    "free": "gemini-2.5-flash",
    "pro": "gemini-2.5-flash"
}

class GeminiIdeaProvider(IdeaProvider):
    def __init__(self, tier: str):
        self.tier = tier
        self.model_name = _DEFAULT_IDEA_MODEL.get(tier, "gemini-2.5-flash")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, request: IdeaRequest) -> GenerationResult[IdeaResponse]:
        start = time.time()
        prompt = f"""Create a story idea based on: "{request.prompt}"

IMPORTANT: Respond ONLY in this exact format (no JSON, no markdown, no code blocks):

Title: [Story Title Here]
Genre: {request.genre or 'Fantasy'}
Tone: {request.tone or 'Adventurous'}
Outline: [Brief 2-3 sentence story summary]
Characters:
[Character Name 1]
[Character Name 2]
[Character Name 3]
Setting: [Brief description of the main setting]

Do not use JSON format. Do not use code blocks. Just plain text with the exact format above."""
        
        resp = self.model.generate_content(prompt)
        text = getattr(resp, 'text', None) or ""
        # naive token approximation
        tokens_in = max(1, len(prompt.split())//0.75)
        tokens_out = max(1, len(text.split())//0.75) if text else 200
        latency_ms = int((time.time() - start) * 1000)
        # rough cost estimate (set to 0 for now)
        cost_usd = 0.0
        
        # Parse the structured text response
        output = self._parse_structured_response(text, request)
        return GenerationResult(output=output, provider="gemini", model=self.model_name, tokens_in=int(tokens_in), tokens_out=int(tokens_out), latency_ms=latency_ms, cost_usd=cost_usd)
    
    def _parse_structured_response(self, text: str, request: IdeaRequest) -> IdeaResponse:
        """Parse a structured text response into IdeaResponse"""
        lines = text.split('\n')
        
        # Default values
        title = "Generated Story Idea"
        genre = request.genre or "Fantasy"
        tone = request.tone or "Adventurous"
        outline = "A creative story idea"
        characters = []
        setting = "An interesting setting"
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect sections
            if line.lower().startswith('title:'):
                title = line.split(':', 1)[1].strip()
            elif line.lower().startswith('genre:'):
                genre = line.split(':', 1)[1].strip()
            elif line.lower().startswith('tone:'):
                tone = line.split(':', 1)[1].strip()
            elif line.lower().startswith('outline:'):
                outline = line.split(':', 1)[1].strip()
                current_section = 'outline'
            elif line.lower().startswith('characters:'):
                current_section = 'characters'
            elif line.lower().startswith('setting:'):
                setting = line.split(':', 1)[1].strip()
                current_section = 'setting'
            elif current_section == 'outline' and line and not line.lower().startswith(('characters:', 'setting:', 'title:', 'genre:', 'tone:')):
                # Continue outline if we're in outline section
                outline += " " + line
            elif current_section == 'characters' and line and not line.lower().startswith(('outline:', 'setting:', 'title:', 'genre:', 'tone:')):
                # Add character if we're in characters section
                if line and not line.lower().startswith(('setting:', 'outline:')):
                    characters.append(line.strip())
            elif current_section == 'setting' and line and not line.lower().startswith(('characters:', 'outline:', 'title:', 'genre:', 'tone:')):
                # Continue setting if we're in setting section
                setting += " " + line
        
        # Clean up the parsed values
        title = title.strip()
        genre = genre.strip()
        tone = tone.strip()
        outline = outline.strip()
        setting = setting.strip()
        
        # Filter out empty character names
        characters = [char.strip() for char in characters if char.strip()]
        
        # If no characters were found, try to extract from the original text
        if not characters:
            # Look for character names in the text
            import re
            # Simple heuristic: look for capitalized words that might be names
            potential_names = re.findall(r'\b[A-Z][a-z]+\b', text)
            characters = potential_names[:4]  # Take first 4 potential names
        
        return IdeaResponse(
            title=title,
            genre=genre,
            tone=tone,
            outline=outline,
            characters=characters if characters else None,
            setting=setting
        )

class GeminiStoryProvider(StoryProvider):
    def __init__(self, tier: str):
        self.tier = tier
        self.model_name = _DEFAULT_STORY_MODEL.get(tier, "gemini-2.5-flash")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, request: StoryRequest) -> GenerationResult[StoryResponse]:
        start = time.time()
        prompt = f"You are a professional story writer. Title: {request.title}\nGenre: {request.genre}\nOutline: {request.outline}\nWrite a structured story."
        resp = self.model.generate_content(prompt)
        text = getattr(resp, 'text', None) or ""
        tokens_in = max(1, len(prompt.split())//0.75)
        tokens_out = max(1, len(text.split())//0.75) if text else 1200
        latency_ms = int((time.time() - start) * 1000)
        cost_usd = 0.0
        from schemas.story import StoryResponse
        output = StoryResponse(story=text or "")
        return GenerationResult(output=output, provider="gemini", model=self.model_name, tokens_in=int(tokens_in), tokens_out=int(tokens_out), latency_ms=latency_ms, cost_usd=cost_usd)
