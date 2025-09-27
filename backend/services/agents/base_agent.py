from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class AgentContext:
    """Context passed between agents during workflow execution"""
    request_id: str
    user_id: str
    user_tier: str
    workflow_id: str
    shared_data: Dict[str, Any]
    created_at: datetime

@dataclass
class AgentResponse:
    """Standard response format for all agents"""
    agent_id: str
    agent_type: str
    success: bool
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    execution_time_ms: int
    created_at: datetime

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, agent_id: str, agent_type: str, name: str, description: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.name = name
        self.description = description
        self.status = "initialized"
        self.created_at = datetime.utcnow()
        self.last_used_at = None
        self.usage_count = 0
        self.error_count = 0
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any], context: AgentContext) -> AgentResponse:
        """Main processing method that each agent must implement"""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for the agent"""
        pass
    
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        return []
    
    def get_requirements(self) -> List[str]:
        """Return list of requirements this agent needs from other agents"""
        return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at,
            "last_used_at": self.last_used_at,
            "usage_count": self.usage_count,
            "error_count": self.error_count
        }
    
    def _update_usage(self):
        """Update agent usage statistics"""
        self.last_used_at = datetime.utcnow()
        self.usage_count += 1
    
    def _update_error(self):
        """Update agent error statistics"""
        self.error_count += 1
    
    def _create_response(self, success: bool, data: Dict[str, Any], 
                        metadata: Dict[str, Any], execution_time_ms: int) -> AgentResponse:
        """Create standardized response"""
        return AgentResponse(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            success=success,
            data=data,
            metadata=metadata,
            execution_time_ms=execution_time_ms,
            created_at=datetime.utcnow()
        )
