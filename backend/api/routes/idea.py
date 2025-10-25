from fastapi import APIRouter, HTTPException, Depends
from schemas.idea import IdeaRequest, IdeaResponse
from services.idea_generator import generate_idea
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

@router.post("/generate-idea", response_model=IdeaResponse)
def generate_story_idea(request: IdeaRequest, user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        allow(user.user_id, user.tier, route_key="idea:generate")
        logger.info(f"Received idea generation request: prompt='{request.prompt[:50]}...', genre={request.genre}")
        
        # Track usage before generating
        start_time = time.time()
        result = generate_idea(request, tier=user.tier)
        end_time = time.time()
        
        # Calculate tokens (estimate based on prompt and response)
        prompt_tokens = len(request.prompt.split()) * 1.3  # Rough estimate
        response_text = f"{result.title} {result.genre} {result.tone} {result.outline}"
        response_tokens = len(response_text.split()) * 1.3  # Rough estimate
        latency_ms = int((end_time - start_time) * 1000)
        
        # Estimate cost (rough calculation)
        cost_usd = (prompt_tokens + response_tokens) * 0.00001  # Very rough estimate
        
        # Log usage to database
        tracker = UsageTracker(db)
        tracker.log_usage(
            user_id=user.user_id,
            feature="idea_generation",
            provider="gemini",
            model="gemini-pro",
            tokens_in=int(prompt_tokens),
            tokens_out=int(response_tokens),
            latency_ms=latency_ms,
            cost_usd=cost_usd
        )
        
        logger.info("Story idea generated successfully")
        return result
    except Exception as e:
        logger.error(f"Error in generate_story_idea endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/idea-examples")
def get_idea_examples():
    examples = [
        {"prompt": "A mysterious lighthouse keeper", "genre": "Mystery", "tone": "Dark and atmospheric"},
        {"prompt": "A time-traveling chef", "genre": "Science Fiction", "tone": "Light-hearted and adventurous"},
        {"prompt": "A magical library that changes every night", "genre": "Fantasy", "tone": "Whimsical and mysterious"},
        {"prompt": "A detective who can see memories", "genre": "Crime", "tone": "Gritty and psychological"}
    ]
    return {"examples": examples}
