import os
import time
import anthropic
from typing import Dict, Any
from schemas.idea import IdeaRequest, IdeaResponse
from schemas.story import StoryRequest, StoryResponse
from .base import GenerationResult, IdeaProvider, StoryProvider
import json

# Anthropic model configurations by tier
_ANTHROPIC_IDEA_MODELS = {
    "free": "claude-3-haiku-20240307",
    "pro": "claude-3-sonnet-20240229",
    "admin": "claude-3-sonnet-20240229"
}

_ANTHROPIC_STORY_MODELS = {
    "free": "claude-3-haiku-20240307", 
    "pro": "claude-3-sonnet-20240229",
    "admin": "claude-3-sonnet-20240229"
}

class AnthropicIdeaProvider(IdeaProvider):
    def __init__(self, tier: str):
        self.tier = tier
        self.model_name = _ANTHROPIC_IDEA_MODELS.get(tier, "claude-3-haiku-20240307")
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def generate(self, request: IdeaRequest) -> GenerationResult[IdeaResponse]:
        start = time.time()
        
        # Build system prompt for idea generation
        system_prompt = """You are a creative story idea generator. Generate compelling story ideas based on user prompts.
        Return your response as JSON with the following structure:
        {
            "title": "Story Title Here",
            "genre": "Genre Here",
            "outline": "Detailed outline here...",
            "characters": "Character descriptions here...",
            "setting": "Setting description here..."
        }"""
        
        # Build user prompt
        user_prompt = f"""
        Generate a story idea based on:
        - Prompt: {request.prompt}
        - Genre: {request.genre or 'Any genre'}
        - Tone: {request.tone or 'Any tone'}
        
        Make it creative, engaging, and well-structured.
        """
        
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=1000,
                temperature=0.8,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            text = response.content[0].text
            tokens_in = response.usage.input_tokens
            tokens_out = response.usage.output_tokens
            latency_ms = int((time.time() - start) * 1000)
            
            # Calculate cost
            cost_usd = self._calculate_cost(tokens_in, tokens_out)
            
            # Parse JSON response
            try:
                idea_data = json.loads(text)
                output = IdeaResponse(
                    title=idea_data.get("title", "Untitled Story"),
                    genre=idea_data.get("genre", request.genre or "General"),
                    outline=idea_data.get("outline", "No outline provided"),
                    characters=idea_data.get("characters"),
                    setting=idea_data.get("setting")
                )
            except json.JSONDecodeError:
                # Fallback parsing
                output = self._parse_text_response(text, request)
            
            return GenerationResult(
                output=output,
                provider="anthropic",
                model=self.model_name,
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                latency_ms=latency_ms,
                cost_usd=cost_usd
            )
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def _parse_text_response(self, text: str, request: IdeaRequest) -> IdeaResponse:
        """Fallback text parsing when JSON fails"""
        lines = text.split('\n')
        title = "Generated Story Idea"
        genre = request.genre or "General"
        
        # Try to extract title
        for line in lines:
            if 'title' in line.lower() and ':' in line:
                title = line.split(':', 1)[1].strip()
                break
        
        return IdeaResponse(
            title=title,
            genre=genre,
            outline=text,
            characters=None,
            setting=None
        )
    
    def _calculate_cost(self, tokens_in: int, tokens_out: int) -> float:
        """Calculate cost based on Anthropic pricing"""
        # Claude-3 Sonnet pricing (as of 2024)
        if "sonnet" in self.model_name:
            input_cost = tokens_in * 0.000003  # $0.003 per 1K tokens
            output_cost = tokens_out * 0.000015  # $0.015 per 1K tokens
        else:  # Claude-3 Haiku
            input_cost = tokens_in * 0.00000025  # $0.00025 per 1K tokens
            output_cost = tokens_out * 0.00000125  # $0.00125 per 1K tokens
        
        return input_cost + output_cost

class AnthropicStoryProvider(StoryProvider):
    def __init__(self, tier: str):
        self.tier = tier
        self.model_name = _ANTHROPIC_STORY_MODELS.get(tier, "claude-3-haiku-20240307")
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def generate(self, request: StoryRequest) -> GenerationResult[StoryResponse]:
        start = time.time()
        
        # Build system prompt for story writing
        system_prompt = """You are a professional story writer. Write engaging, well-structured stories with proper narrative flow, character development, and satisfying conclusions."""
        
        # Build user prompt
        user_prompt = f"""
        Write a complete story with the following details:
        - Title: {request.title}
        - Genre: {request.genre}
        - Outline: {request.outline}
        
        Structure the story with:
        - Introduction and character setup
        - Rising action and conflict
        - Climax and resolution
        - Proper dialogue and descriptions
        
        Make it engaging and well-written.
        """
        
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=2000,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            text = response.content[0].text
            tokens_in = response.usage.input_tokens
            tokens_out = response.usage.output_tokens
            latency_ms = int((time.time() - start) * 1000)
            
            # Calculate cost
            cost_usd = self._calculate_cost(tokens_in, tokens_out)
            
            output = StoryResponse(story=text)
            
            return GenerationResult(
                output=output,
                provider="anthropic",
                model=self.model_name,
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                latency_ms=latency_ms,
                cost_usd=cost_usd
            )
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def _calculate_cost(self, tokens_in: int, tokens_out: int) -> float:
        """Calculate cost based on Anthropic pricing"""
        if "sonnet" in self.model_name:
            input_cost = tokens_in * 0.000003
            output_cost = tokens_out * 0.000015
        else:  # Claude-3 Haiku
            input_cost = tokens_in * 0.00000025
            output_cost = tokens_out * 0.00000125
        
        return input_cost + output_cost
