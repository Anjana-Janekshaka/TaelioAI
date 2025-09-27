from fastapi import APIRouter, HTTPException, Depends
from schemas.story import StoryRequest, StoryResponse
from services.story_writer import generate_story
import logging
from auth.dependencies import get_current_user, UserContext
from services.limits.rate_limiter import allow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/write-story", response_model=StoryResponse)
def write_story(request: StoryRequest, user: UserContext = Depends(get_current_user)):
    try:
        allow(user.user_id, user.tier, route_key="story:write")
        logger.info(f"Received story request: title={request.title}, genre={request.genre}")
        result = generate_story(request, tier=user.tier)
        logger.info("Story generated successfully")
        return result
    except Exception as e:
        logger.error(f"Error in write_story endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
