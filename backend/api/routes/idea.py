from fastapi import APIRouter, HTTPException
from schemas.idea import IdeaRequest, IdeaResponse
from services.idea_generator import generate_idea
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate-idea", response_model=IdeaResponse)
def generate_story_idea(request: IdeaRequest):
    try:
        logger.info(f"Received idea generation request: prompt='{request.prompt[:50]}...', genre={request.genre}")
        result = generate_idea(request)
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
