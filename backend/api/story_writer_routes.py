from fastapi import APIRouter, HTTPException
from schemas.story import StoryRequest, StoryResponse
from services.story_writer import generate_story
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/write-story", response_model=StoryResponse)
def write_story(request: StoryRequest):
    try:
        logger.info(f"Received story request: title={request.title}, genre={request.genre}")
        result = generate_story(request)
        logger.info("Story generated successfully")
        return result
    except Exception as e:
        logger.error(f"Error in write_story endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
