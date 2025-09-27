from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from .idea import IdeaResponse

class WorkflowRequest(BaseModel):
    """Request for multi-agent workflow execution"""
    workflow_type: str  # "full_story_generation", "idea_only", "story_only"
    input_data: Dict[str, Any]
    user_id: str
    user_tier: str

class WorkflowStep(BaseModel):
    """Individual step in a workflow execution"""
    step: int
    agent_id: str
    agent_type: str
    success: bool
    execution_time_ms: int

class WorkflowResponse(BaseModel):
    """Response from multi-agent workflow execution"""
    workflow_id: str
    idea: Optional[IdeaResponse] = None
    story: Optional[Dict[str, Any]] = None
    moderation: Optional[Dict[str, Any]] = None
    quality_assurance: Optional[Dict[str, Any]] = None
    workflow_steps: List[WorkflowStep]
    total_execution_time_ms: int

# Legacy schemas for backward compatibility
class FullStoryRequest(BaseModel):
    prompt: str
    genre: Optional[str] = None
    tone: Optional[str] = None

class FullStoryResponse(BaseModel):
    idea: IdeaResponse
    story: str