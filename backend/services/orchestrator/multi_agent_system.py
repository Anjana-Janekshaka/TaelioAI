from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import asyncio
from services.agents.base_agent import BaseAgent, AgentContext, AgentResponse
from services.agents import (
    IdeaGenerationAgent,
    StoryWritingAgent, 
    ContentModerationAgent,
    QualityAssuranceAgent
)

class MultiAgentSystem:
    """Centralized orchestrator for managing multiple agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_registry: Dict[str, List[str]] = {
            "idea_generation": [],
            "story_writing": [],
            "content_moderation": [],
            "quality_assurance": []
        }
        self.workflow_history: List[Dict[str, Any]] = []
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all available agents"""
        # Register idea generation agents
        idea_agent = IdeaGenerationAgent()
        self.register_agent("idea_generation", idea_agent)
        
        # Register story writing agents
        story_agent = StoryWritingAgent()
        self.register_agent("story_writing", story_agent)
        
        # Register content moderation agents
        mod_agent = ContentModerationAgent()
        self.register_agent("content_moderation", mod_agent)
        
        # Register quality assurance agents
        qa_agent = QualityAssuranceAgent()
        self.register_agent("quality_assurance", qa_agent)
    
    def register_agent(self, agent_type: str, agent: BaseAgent):
        """Register an agent with the system"""
        if agent_type not in self.agent_registry:
            self.agent_registry[agent_type] = []
        
        self.agents[agent.agent_id] = agent
        self.agent_registry[agent_type].append(agent.agent_id)
        
        print(f"[OK] Registered agent: {agent.name} ({agent.agent_id})")
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID"""
        return self.agents.get(agent_id)
    
    def get_agents_by_type(self, agent_type: str) -> List[BaseAgent]:
        """Get all agents of a specific type"""
        agent_ids = self.agent_registry.get(agent_type, [])
        return [self.agents[agent_id] for agent_id in agent_ids if agent_id in self.agents]
    
    def get_best_agent(self, agent_type: str, context: AgentContext) -> Optional[BaseAgent]:
        """Get the best available agent for a specific type"""
        agents = self.get_agents_by_type(agent_type)
        if not agents:
            return None
        
        # For now, return the first available agent
        # In the future, this could implement more sophisticated selection logic
        return agents[0]
    
    async def orchestrate_workflow(self, workflow_type: str, input_data: Dict[str, Any], 
                                 user_id: str, user_tier: str) -> Dict[str, Any]:
        """Orchestrate a multi-agent workflow"""
        workflow_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())
        
        # Create workflow context
        context = AgentContext(
            request_id=request_id,
            user_id=user_id,
            user_tier=user_tier,
            workflow_id=workflow_id,
            shared_data={},
            created_at=datetime.utcnow()
        )
        
        # Record workflow start
        workflow_record = {
            "workflow_id": workflow_id,
            "workflow_type": workflow_type,
            "user_id": user_id,
            "user_tier": user_tier,
            "start_time": datetime.utcnow(),
            "steps": [],
            "status": "running"
        }
        
        try:
            if workflow_type == "full_story_generation":
                result = await self._execute_full_story_workflow(input_data, context)
            elif workflow_type == "idea_only":
                result = await self._execute_idea_generation_workflow(input_data, context)
            elif workflow_type == "story_only":
                result = await self._execute_story_writing_workflow(input_data, context)
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
            
            # Record successful completion
            workflow_record["status"] = "completed"
            workflow_record["end_time"] = datetime.utcnow()
            workflow_record["result"] = result
            
            self.workflow_history.append(workflow_record)
            return result
            
        except Exception as e:
            # Record failure
            workflow_record["status"] = "failed"
            workflow_record["end_time"] = datetime.utcnow()
            workflow_record["error"] = str(e)
            
            self.workflow_history.append(workflow_record)
            raise e
    
    async def _execute_full_story_workflow(self, input_data: Dict[str, Any], 
                                         context: AgentContext) -> Dict[str, Any]:
        """Execute the full story generation workflow"""
        workflow_steps = []
        
        # Step 1: Generate story idea
        idea_agent = self.get_best_agent("idea_generation", context)
        if not idea_agent:
            raise Exception("No idea generation agent available")
        
        idea_response = await idea_agent.process(input_data, context)
        workflow_steps.append({
            "step": 1,
            "agent_id": idea_agent.agent_id,
            "agent_type": idea_agent.agent_type,
            "success": idea_response.success,
            "execution_time_ms": idea_response.execution_time_ms,
            "agent_response": idea_response  # Store complete response with metadata
        })
        
        if not idea_response.success:
            raise Exception(f"Idea generation failed: {idea_response.data}")
        
        # Store idea in shared context
        context.shared_data["idea"] = idea_response.data
        
        # Step 2: Write story
        story_agent = self.get_best_agent("story_writing", context)
        if not story_agent:
            raise Exception("No story writing agent available")
        
        story_input = {
            "title": idea_response.data["title"],
            "genre": idea_response.data["genre"],
            "outline": idea_response.data["outline"]
        }
        
        story_response = await story_agent.process(story_input, context)
        workflow_steps.append({
            "step": 2,
            "agent_id": story_agent.agent_id,
            "agent_type": story_agent.agent_type,
            "success": story_response.success,
            "execution_time_ms": story_response.execution_time_ms,
            "agent_response": story_response  # Store complete response with metadata
        })
        
        if not story_response.success:
            raise Exception(f"Story writing failed: {story_response.data}")
        
        # Step 3: Content moderation
        mod_agent = self.get_best_agent("content_moderation", context)
        if mod_agent:
            mod_input = {
                "content": story_response.data["story"],
                "content_type": "story"
            }
            
            mod_response = await mod_agent.process(mod_input, context)
            workflow_steps.append({
                "step": 3,
                "agent_id": mod_agent.agent_id,
                "agent_type": mod_agent.agent_type,
                "success": mod_response.success,
                "execution_time_ms": mod_response.execution_time_ms,
                "agent_response": mod_response  # Store complete response with metadata
            })
            
            if not mod_response.success or not mod_response.data.get("is_safe", True):
                raise Exception(f"Content moderation failed: {mod_response.data}")
        
        # Step 4: Quality assurance
        qa_agent = self.get_best_agent("quality_assurance", context)
        if qa_agent:
            qa_input = {
                "story": story_response.data["story"],
                "story_metadata": {
                    "title": idea_response.data["title"],
                    "genre": idea_response.data["genre"]
                }
            }
            
            qa_response = await qa_agent.process(qa_input, context)
            workflow_steps.append({
                "step": 4,
                "agent_id": qa_agent.agent_id,
                "agent_type": qa_agent.agent_type,
                "success": qa_response.success,
                "execution_time_ms": qa_response.execution_time_ms,
                "agent_response": qa_response  # Store complete response with metadata
            })
        
        # Assemble final result
        result = {
            "workflow_id": context.workflow_id,
            "idea": idea_response.data,
            "story": story_response.data,
            "moderation": mod_response.data if mod_agent else None,
            "quality_assurance": qa_response.data if qa_agent else None,
            "workflow_steps": workflow_steps,
            "total_execution_time_ms": sum(step["execution_time_ms"] for step in workflow_steps)
        }
        
        return result
    
    async def _execute_idea_generation_workflow(self, input_data: Dict[str, Any], 
                                              context: AgentContext) -> Dict[str, Any]:
        """Execute idea generation only workflow"""
        idea_agent = self.get_best_agent("idea_generation", context)
        if not idea_agent:
            raise Exception("No idea generation agent available")
        
        idea_response = await idea_agent.process(input_data, context)
        
        return {
            "workflow_id": context.workflow_id,
            "idea": idea_response.data,
            "workflow_steps": [{
                "step": 1,
                "agent_id": idea_agent.agent_id,
                "agent_type": idea_agent.agent_type,
                "success": idea_response.success,
                "execution_time_ms": idea_response.execution_time_ms,
                "agent_response": idea_response  # Store complete response with metadata
            }],
            "total_execution_time_ms": idea_response.execution_time_ms
        }
    
    async def _execute_story_writing_workflow(self, input_data: Dict[str, Any], 
                                            context: AgentContext) -> Dict[str, Any]:
        """Execute story writing only workflow"""
        story_agent = self.get_best_agent("story_writing", context)
        if not story_agent:
            raise Exception("No story writing agent available")
        
        story_response = await story_agent.process(input_data, context)
        
        return {
            "workflow_id": context.workflow_id,
            "story": story_response.data,
            "workflow_steps": [{
                "step": 1,
                "agent_id": story_agent.agent_id,
                "agent_type": story_agent.agent_type,
                "success": story_response.success,
                "execution_time_ms": story_response.execution_time_ms,
                "agent_response": story_response  # Store complete response with metadata
            }],
            "total_execution_time_ms": story_response.execution_time_ms
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        agent_statuses = {}
        for agent_id, agent in self.agents.items():
            agent_statuses[agent_id] = agent.get_status()
        
        return {
            "total_agents": len(self.agents),
            "agent_types": list(self.agent_registry.keys()),
            "agent_statuses": agent_statuses,
            "workflow_history_count": len(self.workflow_history),
            "system_status": "operational"
        }
    
    def get_workflow_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent workflow history"""
        return self.workflow_history[-limit:] if self.workflow_history else []

# Global instance
multi_agent_system = MultiAgentSystem()
