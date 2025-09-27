from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from db.database import get_db
from auth.dependencies import get_current_user, UserContext
from services.limits.rate_limiter import allow
from services.orchestrator import multi_agent_system
from schemas.workflow import WorkflowRequest, WorkflowResponse, FullStoryRequest
from metrics.usage import log_usage
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/orchestrated-workflow", response_model=WorkflowResponse)
async def execute_orchestrated_workflow(
    request: WorkflowRequest,
    current_user: UserContext = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a multi-agent workflow using the orchestrator"""
    try:
        # Rate limiting
        allow(current_user.user_id, current_user.tier, route_key="orchestrated_workflow")
        
        logger.info(f"Executing orchestrated workflow: {request.workflow_type} for user {current_user.user_id}")
        
        # Execute workflow using multi-agent system
        result = await multi_agent_system.orchestrate_workflow(
            workflow_type=request.workflow_type,
            input_data=request.input_data,
            user_id=current_user.user_id,
            user_tier=current_user.tier
        )
        
        # Log usage for each step
        for step in result.get("workflow_steps", []):
            log_usage(
                user_id=current_user.user_id,
                feature=step["agent_type"],
                provider="multi_agent",
                model=f"agent_{step['agent_id']}",
                tokens_in=0,  # Will be updated by individual agents
                tokens_out=0,  # Will be updated by individual agents
                latency_ms=step["execution_time_ms"],
                cost_usd=0.0,  # Will be calculated by individual agents
                db=db,
                user_tier=current_user.tier  # Pass user tier for Prometheus metrics
            )
        
        logger.info(f"Orchestrated workflow completed successfully: {result['workflow_id']}")
        return result
        
    except Exception as e:
        logger.error(f"Error in orchestrated workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

@router.post("/full-story-orchestrated")
async def generate_full_story_orchestrated(
    request: FullStoryRequest,
    current_user: UserContext = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate full story using orchestrated multi-agent workflow"""
    try:
        # Rate limiting
        allow(current_user.user_id, current_user.tier, route_key="full_story_orchestrated")
        
        # Create workflow request
        workflow_request = WorkflowRequest(
            workflow_type="full_story_generation",
            input_data={
                "prompt": request.prompt,
                "genre": request.genre,
                "tone": request.tone
            },
            user_id=current_user.user_id,
            user_tier=current_user.tier
        )
        
        # Execute workflow
        result = await multi_agent_system.orchestrate_workflow(
            workflow_type="full_story_generation",
            input_data=workflow_request.input_data,
            user_id=current_user.user_id,
            user_tier=current_user.tier
        )
        
        logger.info(f"Full story generation completed: {result['workflow_id']}")
        return result
        
    except Exception as e:
        logger.error(f"Error in full story generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")

@router.post("/idea-only-orchestrated")
async def generate_idea_only_orchestrated(
    request: FullStoryRequest,
    current_user: UserContext = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate idea only using orchestrated multi-agent workflow"""
    try:
        # Rate limiting
        allow(current_user.user_id, current_user.tier, route_key="idea_only_orchestrated")
        
        # Execute workflow
        result = await multi_agent_system.orchestrate_workflow(
            workflow_type="idea_only",
            input_data={
                "prompt": request.prompt,
                "genre": request.genre,
                "tone": request.tone
            },
            user_id=current_user.user_id,
            user_tier=current_user.tier
        )
        
        logger.info(f"Idea generation completed: {result['workflow_id']}")
        return result
        
    except Exception as e:
        logger.error(f"Error in idea generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Idea generation failed: {str(e)}")

@router.get("/system-status")
async def get_system_status(
    current_user: UserContext = Depends(get_current_user)
):
    """Get multi-agent system status"""
    if current_user.tier not in ["admin", "pro"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return multi_agent_system.get_system_status()

@router.get("/workflow-history")
async def get_workflow_history(
    limit: int = 10,
    current_user: UserContext = Depends(get_current_user)
):
    """Get recent workflow execution history"""
    if current_user.tier not in ["admin", "pro"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "workflow_history": multi_agent_system.get_workflow_history(limit=limit)
    }
