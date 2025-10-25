from fastapi import APIRouter, HTTPException, Depends
from schemas.workflow import FullStoryRequest, FullStoryResponse
from services.full_story_workflow import generate_full_story, generate_idea_only
import logging
from auth.dependencies import get_current_user, UserContext
from services.limits.rate_limiter import allow
from services.usage_tracker import UsageTracker
from db.database import get_db
from sqlalchemy.orm import Session
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate-full-story", response_model=FullStoryResponse)
def create_full_story(request: FullStoryRequest, user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        allow(user.user_id, user.tier, route_key="workflow:full")
        logger.info(f"Received full story request: prompt='{request.prompt[:50]}...'")
        
        # Track usage before generating
        start_time = time.time()
        result = generate_full_story(request)
        end_time = time.time()
        
        # Calculate tokens (estimate based on prompt and response)
        prompt_tokens = len(request.prompt.split()) * 1.3  # Rough estimate
        response_tokens = len(result.story.split()) * 1.3  # Rough estimate
        latency_ms = int((end_time - start_time) * 1000)
        
        # Estimate cost (rough calculation)
        cost_usd = (prompt_tokens + response_tokens) * 0.00001  # Very rough estimate
        
        # Log usage to database
        tracker = UsageTracker(db)
        tracker.log_usage(
            user_id=user.user_id,
            feature="full_workflow",
            provider="gemini",
            model="gemini-pro",
            tokens_in=int(prompt_tokens),
            tokens_out=int(response_tokens),
            latency_ms=latency_ms,
            cost_usd=cost_usd
        )
        
        logger.info("Full story workflow completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error in full story workflow endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/generate-idea-only", response_model=FullStoryResponse)
def create_idea_only(request: FullStoryRequest, user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        allow(user.user_id, user.tier, route_key="workflow:idea_only")
        logger.info(f"Received idea-only request: prompt='{request.prompt[:50]}...'")
        
        # Track usage before generating
        start_time = time.time()
        result = generate_idea_only(request)
        end_time = time.time()
        
        # Calculate tokens (estimate based on prompt and response)
        prompt_tokens = len(request.prompt.split()) * 1.3  # Rough estimate
        response_tokens = len(result.idea.split()) * 1.3  # Rough estimate
        latency_ms = int((end_time - start_time) * 1000)
        
        # Estimate cost (rough calculation)
        cost_usd = (prompt_tokens + response_tokens) * 0.00001  # Very rough estimate
        
        # Log usage to database
        tracker = UsageTracker(db)
        tracker.log_usage(
            user_id=user.user_id,
            feature="idea_only_workflow",
            provider="gemini",
            model="gemini-pro",
            tokens_in=int(prompt_tokens),
            tokens_out=int(response_tokens),
            latency_ms=latency_ms,
            cost_usd=cost_usd
        )
        
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
