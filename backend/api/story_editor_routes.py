# backend/api/story_editor_routes.py
from fastapi import APIRouter, Body
from services.story_editor import edit_story_with_gemini

router = APIRouter()

@router.post("/edit")
async def edit_story_endpoint(text: str = Body(..., embed=True)):
    """
    Endpoint to improve story text using Google Gemini API.
    """
    edited = edit_story_with_gemini(text)
    return {"original": text, "edited": edited}
