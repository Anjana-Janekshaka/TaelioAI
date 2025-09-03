from fastapi import APIRouter
from schemas.story import StoryRequest, StoryResponse
from services.story_writer import generate_story

router = APIRouter()

@router.post("/write-story", response_model=StoryResponse)
def write_story(request: StoryRequest):
    return generate_story(request)
