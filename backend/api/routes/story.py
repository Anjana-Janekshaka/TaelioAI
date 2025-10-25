from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from schemas.story import StoryRequest, StoryResponse
from services.story_writer import generate_story, generate_story_streaming
import logging
from auth.dependencies import get_current_user, UserContext
from services.limits.rate_limiter import allow
import json
import asyncio

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

@router.post("/write-story-stream")
async def write_story_streaming(
    request: StoryRequest, 
    user: UserContext = Depends(get_current_user),
    streaming_speed: str = "normal"
):
    """Stream story generation with Server-Sent Events (SSE)"""
    try:
        allow(user.user_id, user.tier, route_key="story:write")
        logger.info(f"Received streaming story request: title={request.title}, genre={request.genre}, speed={streaming_speed}")
        
        async def generate():
            try:
                async for chunk in generate_story_streaming(request, tier=user.tier, streaming_speed=streaming_speed):
                    # Format as Server-Sent Events
                    yield f"data: {json.dumps(chunk)}\n\n"
                # Send completion signal
                yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            except Exception as e:
                logger.error(f"Error in streaming story generation: {str(e)}")
                error_chunk = {
                    'type': 'error',
                    'error': str(e)
                }
                yield f"data: {json.dumps(error_chunk)}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
    except Exception as e:
        logger.error(f"Error in write_story_streaming endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
