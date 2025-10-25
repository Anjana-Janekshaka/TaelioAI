from fastapi import APIRouter, HTTPException, Depends
from schemas.story import StoryRequest, StoryResponse
from services.story_writer import generate_story
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

@router.post("/write-story", response_model=StoryResponse)
def write_story(request: StoryRequest, user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        allow(user.user_id, user.tier, route_key="story:write")
        logger.info(f"Received story request: title={request.title}, genre={request.genre}")
        
        # Track usage before generating
        start_time = time.time()
        result = generate_story(request, tier=user.tier)
        end_time = time.time()
        
        # Calculate tokens (estimate based on prompt and response)
        prompt_text = f"{request.title} {request.genre} {request.outline}"
        prompt_tokens = len(prompt_text.split()) * 1.3  # Rough estimate
        response_tokens = len(result.story.split()) * 1.3  # Rough estimate
        latency_ms = int((end_time - start_time) * 1000)
        
        # Estimate cost (rough calculation)
        cost_usd = (prompt_tokens + response_tokens) * 0.00001  # Very rough estimate
        
        # Log usage to database
        tracker = UsageTracker(db)
        tracker.log_usage(
            user_id=user.user_id,
            feature="story_writing",
            provider="gemini",
            model="gemini-pro",
            tokens_in=int(prompt_tokens),
            tokens_out=int(response_tokens),
            latency_ms=latency_ms,
            cost_usd=cost_usd
        )
        
        logger.info("Story generated successfully")
        return result
    except Exception as e:
        logger.error(f"Error in write_story endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
