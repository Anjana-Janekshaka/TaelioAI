import time
from typing import Dict, Any
from .base_agent import BaseAgent, AgentContext, AgentResponse
from services.providers.router import router
from schemas.idea import IdeaRequest, IdeaResponse

class IdeaGenerationAgent(BaseAgent):
    """Agent specialized in generating creative story ideas"""
    
    def __init__(self):
        super().__init__(
            agent_id="idea_gen_001",
            agent_type="idea_generator",
            name="Creative Idea Generator",
            description="Generates creative story ideas from simple prompts"
        )
        self.status = "ready"
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for idea generation"""
        required_fields = ["prompt"]
        return all(field in input_data for field in required_fields)
    
    def get_capabilities(self) -> list:
        return [
            "story_idea_generation",
            "genre_classification",
            "character_creation",
            "setting_development",
            "plot_outline_creation"
        ]
    
    def get_requirements(self) -> list:
        return [
            "user_prompt",
            "optional_genre",
            "optional_tone"
        ]
    
    async def process(self, input_data: Dict[str, Any], context: AgentContext) -> AgentResponse:
        """Generate a story idea from the input prompt"""
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
            
            # Create idea request
            idea_request = IdeaRequest(
                prompt=input_data["prompt"],
                genre=input_data.get("genre"),
                tone=input_data.get("tone")
            )
            
            # Generate idea using provider router
            provider = router.select(task="idea", tier=context.user_tier)
            result = provider.generate(idea_request)
            
            # Update usage statistics
            self._update_usage()
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Create response data
            response_data = {
                "title": result.output.title,
                "genre": result.output.genre,
                "outline": result.output.outline,
                "characters": result.output.characters,
                "setting": result.output.setting
            }
            
            # Create metadata
            metadata = {
                "provider": result.provider,
                "model": result.model,
                "tokens_in": result.tokens_in,
                "tokens_out": result.tokens_out,
                "cost_usd": result.cost_usd,
                "user_tier": context.user_tier
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
