import os
import time
import openai
from typing import Dict, Any, AsyncGenerator
from schemas.idea import IdeaRequest, IdeaResponse
from schemas.story import StoryRequest, StoryResponse
from .base import GenerationResult, IdeaProvider, StoryProvider
import json
import asyncio

# OpenAI model configurations by tier
_OPENAI_IDEA_MODELS = {
    "free": "gpt-3.5-turbo",
    "pro": "gpt-4",
    "admin": "gpt-4"
}

_OPENAI_STORY_MODELS = {
    "free": "gpt-3.5-turbo",
    "pro": "gpt-4",
    "admin": "gpt-4"
}

class OpenAIIdeaProvider(IdeaProvider):
    def __init__(self, tier: str):
        self.tier = tier
        self.model_name = _OPENAI_IDEA_MODELS.get(tier, "gpt-3.5-turbo")
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
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
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            text = response.choices[0].message.content
            tokens_in = response.usage.prompt_tokens
            tokens_out = response.usage.completion_tokens
            latency_ms = int((time.time() - start) * 1000)
            
            # Calculate cost (rough estimates)
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
                provider="openai",
                model=self.model_name,
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                latency_ms=latency_ms,
                cost_usd=cost_usd
            )
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
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
        """Calculate cost based on OpenAI pricing"""
        # GPT-4 pricing (as of 2024)
        if "gpt-4" in self.model_name:
            input_cost = tokens_in * 0.00003  # $0.03 per 1K tokens
            output_cost = tokens_out * 0.00006  # $0.06 per 1K tokens
        else:  # GPT-3.5-turbo
            input_cost = tokens_in * 0.0000015  # $0.0015 per 1K tokens
            output_cost = tokens_out * 0.000002  # $0.002 per 1K tokens
        
        return input_cost + output_cost

class OpenAIStoryProvider(StoryProvider):
    def __init__(self, tier: str):
        self.tier = tier
        self.model_name = _OPENAI_STORY_MODELS.get(tier, "gpt-3.5-turbo")
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate(self, request: StoryRequest) -> GenerationResult[StoryResponse]:
        start = time.time()
        
        # Build system prompt for story writing
        system_prompt = """You are a professional story writer. Write engaging, well-structured stories with proper narrative flow, character development, and satisfying conclusions."""
        
        # Build user prompt with optional fields
        optional_details = []
        if request.tone:
            optional_details.append(f"- Tone: {request.tone}")
        if request.characters:
            optional_details.append(f"- Characters: {request.characters}")
        if request.setting:
            optional_details.append(f"- Setting: {request.setting}")
        
        optional_section = "\n".join(optional_details) if optional_details else ""
        
        user_prompt = f"""
        Write a complete story with the following details:
        - Title: {request.title}
        - Genre: {request.genre}
        - Outline: {request.outline}
        {optional_section}
        
        Structure the story with:
        - Introduction and character setup
        - Rising action and conflict
        - Climax and resolution
        - Proper dialogue and descriptions
        
        Make it engaging and well-written.{" When provided, ensure the tone, characters, and setting match the details above." if optional_section else ""}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            text = response.choices[0].message.content
            tokens_in = response.usage.prompt_tokens
            tokens_out = response.usage.completion_tokens
            latency_ms = int((time.time() - start) * 1000)
            
            # Calculate cost
            cost_usd = self._calculate_cost(tokens_in, tokens_out)
            
            output = StoryResponse(story=text)
            
            return GenerationResult(
                output=output,
                provider="openai",
                model=self.model_name,
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                latency_ms=latency_ms,
                cost_usd=cost_usd
            )
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _calculate_cost(self, tokens_in: int, tokens_out: int) -> float:
        """Calculate cost based on OpenAI pricing"""
        if "gpt-4" in self.model_name:
            input_cost = tokens_in * 0.00003
            output_cost = tokens_out * 0.00006
        else:  # GPT-3.5-turbo
            input_cost = tokens_in * 0.0000015
            output_cost = tokens_out * 0.000002
        
        return input_cost + output_cost

    async def generate_streaming(self, request: StoryRequest) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate story with streaming support"""
        start = time.time()
        
        # Build system prompt for story writing
        system_prompt = """You are a professional story writer. Write engaging, well-structured stories with proper narrative flow, character development, and satisfying conclusions."""
        
        # Build user prompt with optional fields
        optional_details = []
        if request.tone:
            optional_details.append(f"- Tone: {request.tone}")
        if request.characters:
            optional_details.append(f"- Characters: {request.characters}")
        if request.setting:
            optional_details.append(f"- Setting: {request.setting}")
        
        optional_section = "\n".join(optional_details) if optional_details else ""
        
        user_prompt = f"""
        Write a complete story with the following details:
        - Title: {request.title}
        - Genre: {request.genre}
        - Outline: {request.outline}
        {optional_section}
        
        Structure the story with:
        - Introduction and character setup
        - Rising action and conflict
        - Climax and resolution
        - Proper dialogue and descriptions
        
        Make it engaging and well-written.{" When provided, ensure the tone, characters, and setting match the details above." if optional_section else ""}
        """
        
        try:
            # Use streaming API
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                stream=True
            )
            
            full_content = ""
            tokens_in = 0
            tokens_out = 0
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_content += content
                    tokens_out += 1  # Rough estimate
                    
                    yield {
                        'type': 'content',
                        'content': content,
                        'is_final': False
                    }
                    
                    # Add small delay to make streaming more readable
                    await asyncio.sleep(0.02)
                
                # Update usage if available
                if hasattr(chunk, 'usage') and chunk.usage:
                    tokens_in = chunk.usage.prompt_tokens or tokens_in
                    tokens_out = chunk.usage.completion_tokens or tokens_out
            
            # Send final metadata
            latency_ms = int((time.time() - start) * 1000)
            cost_usd = self._calculate_cost(tokens_in, tokens_out)
            
            yield {
                'type': 'metadata',
                'provider': 'openai',
                'model': self.model_name,
                'tokens_in': tokens_in,
                'tokens_out': tokens_out,
                'latency_ms': latency_ms,
                'cost_usd': cost_usd,
                'is_final': True
            }
            
        except Exception as e:
            yield {
                'type': 'error',
                'error': f"OpenAI streaming API error: {str(e)}"
            }
