from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from services.agents.story_editor_agent import StoryEditorAgent
from services.agents.base_agent import AgentContext
from auth.dependencies import get_current_user
from db.models import User
from datetime import datetime
import uuid

router = APIRouter(tags=["story-editor"])

class StoryEditRequest(BaseModel):
    story: str
    edit_instructions: str
    title: str = "Edited Story"
    genre: str = "General"

class StoryEditResponse(BaseModel):
    success: bool
    edited_story: str
    original_story: str
    edit_instructions: str
    title: str
    genre: str
    metadata: Dict[str, Any]

@router.post("/edit", response_model=StoryEditResponse)
async def edit_story(
    request: StoryEditRequest,
    current_user: User = Depends(get_current_user)
):
    """Edit a story using the story editor agent"""
    
    try:
        # Create agent context
        context = AgentContext(
            request_id=str(uuid.uuid4()),
            user_id=str(current_user.user_id),
            user_tier=current_user.role,
            workflow_id=str(uuid.uuid4()),
            shared_data={},
            created_at=datetime.utcnow()
        )
        
        # Create story editor agent
        editor_agent = StoryEditorAgent()
        
        # Prepare input data
        input_data = {
            "story": request.story,
            "edit_instructions": request.edit_instructions,
            "title": request.title,
            "genre": request.genre
        }
        
        # Process the edit request
        response = await editor_agent.process(input_data, context)
        
        if not response.success:
            raise HTTPException(
                status_code=400,
                detail=f"Story editing failed: {response.data.get('error', 'Unknown error')}"
            )
        
        return StoryEditResponse(
            success=True,
            edited_story=response.data["edited_story"],
            original_story=response.data["original_story"],
            edit_instructions=response.data["edit_instructions"],
            title=response.data["title"],
            genre=response.data["genre"],
            metadata=response.metadata
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/edit-dev", response_model=StoryEditResponse)
async def edit_story_dev(request: StoryEditRequest):
    """Edit a story using the story editor agent (development mode - no auth required)"""
    
    try:
        # Create agent context with default values for development
        context = AgentContext(
            request_id=str(uuid.uuid4()),
            user_id="dev-user-001",
            user_tier="free",
            workflow_id=str(uuid.uuid4()),
            shared_data={},
            created_at=datetime.utcnow()
        )
        
        # Create story editor agent
        editor_agent = StoryEditorAgent()
        
        # Prepare input data
        input_data = {
            "story": request.story,
            "edit_instructions": request.edit_instructions,
            "title": request.title,
            "genre": request.genre
        }
        
        # Process the edit request
        response = await editor_agent.process(input_data, context)
        
        if not response.success:
            raise HTTPException(
                status_code=400,
                detail=f"Story editing failed: {response.data.get('error', 'Unknown error')}"
            )
        
        return StoryEditResponse(
            success=True,
            edited_story=response.data["edited_story"],
            original_story=response.data["original_story"],
            edit_instructions=response.data["edit_instructions"],
            title=response.data["title"],
            genre=response.data["genre"],
            metadata=response.metadata
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/capabilities")
async def get_editor_capabilities():
    """Get the capabilities of the story editor agent"""
    
    try:
        editor_agent = StoryEditorAgent()
        
        return {
            "success": True,
            "capabilities": editor_agent.get_capabilities(),
            "requirements": editor_agent.get_requirements(),
            "agent_info": editor_agent.get_status()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get capabilities: {str(e)}"
        )
