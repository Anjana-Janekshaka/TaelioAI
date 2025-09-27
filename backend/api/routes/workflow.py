from fastapi import APIRouter, HTTPException, Depends
from schemas.workflow import FullStoryRequest, FullStoryResponse
from services.full_story_workflow import generate_full_story, generate_idea_only
import logging
from auth.dependencies import get_current_user, UserContext
from services.limits.rate_limiter import allow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate-full-story", response_model=FullStoryResponse)
def create_full_story(request: FullStoryRequest, user: UserContext = Depends(get_current_user)):
    try:
        allow(user.user_id, user.tier, route_key="workflow:full")
        logger.info(f"Received full story request: prompt='{request.prompt[:50]}...'")
        # pass tier via environment to underlying services through dependency? simplest: set in services to free for now
        result = generate_full_story(request)
        logger.info("Full story workflow completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error in full story workflow endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/generate-idea-only", response_model=FullStoryResponse)
def create_idea_only(request: FullStoryRequest, user: UserContext = Depends(get_current_user)):
    try:
        allow(user.user_id, user.tier, route_key="workflow:idea_only")
        logger.info(f"Received idea-only request: prompt='{request.prompt[:50]}...'")
        result = generate_idea_only(request)
        logger.info("Idea generation completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error in idea-only endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/workflow-info")
def get_workflow_info():
    return {
        "workflow": {
            "step_1": {"agent": "Idea Generator", "input": "User prompt", "output": "Story idea (title, genre, outline, characters, setting)"},
            "step_2": {"agent": "Story Writer", "input": "Story idea from step 1", "output": "Complete story"}
        },
        "endpoints": {
            "full_workflow": "/workflow/generate-full-story",
            "idea_only": "/workflow/generate-idea-only",
            "individual_idea": "/idea/generate-idea",
            "individual_story": "/story/write-story"
        }
    }
