import time
from typing import Dict, Any
from .base_agent import BaseAgent, AgentContext, AgentResponse
from services.providers.router import router
from schemas.story import StoryRequest, StoryResponse

class StoryEditorAgent(BaseAgent):
    """Agent specialized in editing and refining existing stories"""
    
    def __init__(self):
        super().__init__(
            agent_id="story_editor_001",
            agent_type="story_editor",
            name="Story Editor",
            description="Edits and refines existing stories with user-specified changes"
        )
        self.status = "ready"
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for story editing"""
        required_fields = ["story", "edit_instructions"]
        return all(field in input_data for field in required_fields)
    
    def get_capabilities(self) -> list:
        return [
            "story_editing",
            "content_refinement",
            "style_improvement",
            "plot_adjustment",
            "character_development",
            "dialogue_enhancement",
            "scene_improvement"
        ]
    
    def get_requirements(self) -> list:
        return [
            "original_story",
            "edit_instructions",
            "optional_style_preferences",
            "optional_length_requirements"
        ]
    
    async def process(self, input_data: Dict[str, Any], context: AgentContext) -> AgentResponse:
        """Edit a story based on user instructions"""
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
            
            # Create story request for editing
            story_request = StoryRequest(
                title=input_data.get("title", "Edited Story"),
                genre=input_data.get("genre", "General"),
                outline=input_data["edit_instructions"]
            )
            
            # For editing, we'll use a custom prompt that includes the original story
            edit_prompt = f"""
            Original Story:
            {input_data['story']}
            
            Edit Instructions:
            {input_data['edit_instructions']}
            
            Please edit the story according to the instructions above. Maintain the core narrative while implementing the requested changes.
            """
            
            # Generate edited story using provider router
            provider = router.select(task="story", tier=context.user_tier)
            
            # Create a custom request for editing
            edit_request = StoryRequest(
                title=input_data.get("title", "Edited Story"),
                genre=input_data.get("genre", "General"),
                outline=edit_prompt
            )
            
            result = provider.generate(edit_request)
            
            # Update usage statistics
            self._update_usage()
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Create response data
            response_data = {
                "edited_story": result.output.story,
                "original_story": input_data["story"],
                "edit_instructions": input_data["edit_instructions"],
                "title": input_data.get("title", "Edited Story"),
                "genre": input_data.get("genre", "General")
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
                "word_count": len(result.output.story.split()),
                "edit_type": "story_refinement"
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
