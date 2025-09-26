from schemas.workflow import FullStoryRequest, FullStoryResponse
from schemas.idea import IdeaRequest
from schemas.story import StoryRequest
from services.idea_generator import generate_idea
from services.story_writer import generate_story
import logging

logger = logging.getLogger(__name__)

def generate_full_story(request: FullStoryRequest) -> FullStoryResponse:
    """
    Complete workflow that combines Idea Generator + Story Writer.
    This implements the multi-agent system from the flowchart.
    
    Flow:
    1. User Prompt -> Idea Generator Agent -> Story Idea
    2. Story Idea -> Story Writer Agent -> Full Story
    3. Return both idea and story
    """
    try:
        logger.info(f"Starting full story workflow for prompt: '{request.prompt[:50]}...'")
        
        # Step 1: Generate story idea using Idea Generator Agent
        logger.info("Step 1: Generating story idea...")
        idea_request = IdeaRequest(
            prompt=request.prompt,
            genre=request.genre,
            tone=request.tone
        )
        idea_response = generate_idea(idea_request)
        logger.info(f"✅ Story idea generated: '{idea_response.title}'")
        
        # Step 2: Generate full story using Story Writer Agent
        logger.info("Step 2: Expanding idea into full story...")
        story_request = StoryRequest(
            title=idea_response.title,
            genre=idea_response.genre,
            outline=idea_response.outline
        )
        story_response = generate_story(story_request)
        logger.info("✅ Full story generated successfully")
        
        # Step 3: Return combined result
        return FullStoryResponse(
            idea=idea_response,
            story=story_response.story
        )
        
    except Exception as e:
        logger.error(f"Error in full story workflow: {str(e)}")
        raise Exception(f"Error in full story generation workflow: {str(e)}")

def generate_idea_only(request: FullStoryRequest) -> FullStoryResponse:
    """
    Generate only the story idea (for testing or when user wants just the idea).
    """
    try:
        logger.info(f"Generating idea only for prompt: '{request.prompt[:50]}...'")
        
        idea_request = IdeaRequest(
            prompt=request.prompt,
            genre=request.genre,
            tone=request.tone
        )
        idea_response = generate_idea(idea_request)
        
        # Return with empty story
        return FullStoryResponse(
            idea=idea_response,
            story=""
        )
        
    except Exception as e:
        logger.error(f"Error in idea-only generation: {str(e)}")
        raise Exception(f"Error generating story idea: {str(e)}")
