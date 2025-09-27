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
        prompt = f"Generate a JSON idea with title, genre, outline, characters, setting. Prompt: {request.prompt}. Genre: {request.genre or 'Any'}. Tone: {request.tone or 'Any'}"
        resp = self.model.generate_content(prompt)
        text = getattr(resp, 'text', None) or ""
        # naive token approximation
        tokens_in = max(1, len(prompt.split())//0.75)
        tokens_out = max(1, len(text.split())//0.75) if text else 200
        latency_ms = int((time.time() - start) * 1000)
        # rough cost estimate (set to 0 for now)
        cost_usd = 0.0
        # parse via existing service? keep simple: reuse existing parsing path later
        from services.idea_generator import _parse_text_response
        output = _parse_text_response(text or "", request)
        return GenerationResult(output=output, provider="gemini", model=self.model_name, tokens_in=int(tokens_in), tokens_out=int(tokens_out), latency_ms=latency_ms, cost_usd=cost_usd)

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
