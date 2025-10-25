import time
from typing import Dict, Any
from .base_agent import BaseAgent, AgentContext, AgentResponse
from services.providers.router import router
from schemas.story import StoryRequest, StoryResponse

class StoryWritingAgent(BaseAgent):
    """Agent specialized in writing full stories from ideas"""
    
    def __init__(self):
        super().__init__(
            agent_id="story_writer_001",
            agent_type="story_writer",
            name="Story Writer",
            description="Writes complete stories from story ideas and outlines"
        )
        self.status = "ready"
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for story writing"""
        required_fields = ["title", "genre", "outline"]
        return all(field in input_data for field in required_fields)
    
    def get_capabilities(self) -> list:
        return [
            "story_writing",
            "narrative_structure",
            "character_development",
            "plot_progression",
            "dialogue_creation",
            "scene_descriptions"
        ]
    
    def get_requirements(self) -> list:
        return [
            "story_title",
            "story_genre",
            "story_outline",
            "optional_characters",
            "optional_setting"
        ]
    
    async def process(self, input_data: Dict[str, Any], context: AgentContext) -> AgentResponse:
        """Write a complete story from the input idea"""
        start_time = time.time()
        
        try:
            # Validate input
            if not self.validate_input(input_data):
                self._update_error()
                return self._create_response(
                    success=False,
                    data={"error": "Invalid input data"},
                    metadata={"error_type": "validation_error"},
                    execution_time_ms=0
                )
            
            # Create story request with optional fields
            story_request = StoryRequest(
                title=input_data["title"],
                genre=input_data["genre"],
                outline=input_data["outline"],
                tone=input_data.get("tone"),
                characters=input_data.get("characters"),
                setting=input_data.get("setting")
            )
            
            # Generate story using provider router
            provider = router.select(task="story", tier=context.user_tier)
            result = provider.generate(story_request)
            
            # Update usage statistics
            self._update_usage()
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Create response data
            response_data = {
                "story": result.output.story,
                "title": input_data["title"],
                "genre": input_data["genre"]
            }
            
            # Create metadata
            metadata = {
                "provider": result.provider,
                "model": result.model,
                "tokens_in": result.tokens_in,
                "tokens_out": result.tokens_out,
                "cost_usd": result.cost_usd,
                "user_tier": context.user_tier,
                "story_length": len(result.output.story),
                "word_count": len(result.output.story.split())
            }
            
            return self._create_response(
                success=True,
                data=response_data,
                metadata=metadata,
                execution_time_ms=execution_time_ms
            )
            
        except Exception as e:
            self._update_error()
            execution_time_ms = int((time.time() - start_time) * 1000)
            return self._create_response(
                success=False,
                data={"error": str(e)},
                metadata={"error_type": "processing_error"},
                execution_time_ms=execution_time_ms
            )
