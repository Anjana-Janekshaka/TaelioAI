import time
import re
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentContext, AgentResponse

class ContentModerationAgent(BaseAgent):
    """Agent specialized in content moderation and safety checks"""
    
    def __init__(self):
        super().__init__(
            agent_id="content_mod_001",
            agent_type="content_moderator",
            name="Content Moderator",
            description="Moderates content for safety, appropriateness, and policy compliance"
        )
        self.status = "ready"
        
        # Define content policies
        self.inappropriate_keywords = [
            "violence", "hate", "discrimination", "harassment",
            "explicit", "adult", "inappropriate", "offensive"
        ]
        
        self.safety_patterns = [
            r'\b(violence|harm|danger)\b',
            r'\b(hate|discrimination)\b',
            r'\b(explicit|adult|sexual)\b'
        ]
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for content moderation"""
        required_fields = ["content"]
        return all(field in input_data for field in required_fields)
    
    def get_capabilities(self) -> list:
        return [
            "content_safety_check",
            "inappropriate_content_detection",
            "policy_compliance_verification",
            "content_quality_assessment",
            "safety_scoring"
        ]
    
    def get_requirements(self) -> list:
        return [
            "content_text",
            "optional_content_type",
            "optional_safety_level"
        ]
    
    async def process(self, input_data: Dict[str, Any], context: AgentContext) -> AgentResponse:
        """Moderate content for safety and appropriateness"""
        start_time = time.time()
        
        try:
            # Validate input
            if not self.validate_input(input_data):
                self._update_error()
                return self._create_response(
                    success=False,
                    data={"error": "Invalid input data"},
                    metadata={"error_type": "validation_error"},
                    execution_time_ms=0
                )
            
            content = input_data["content"]
            content_type = input_data.get("content_type", "story")
            safety_level = input_data.get("safety_level", "standard")
            
            # Perform content moderation checks
            moderation_result = self._moderate_content(content, content_type, safety_level)
            
            # Update usage statistics
            self._update_usage()
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Create response data
            response_data = {
                "is_safe": moderation_result["is_safe"],
                "safety_score": moderation_result["safety_score"],
                "violations": moderation_result["violations"],
                "recommendations": moderation_result["recommendations"],
                "moderated_content": moderation_result.get("moderated_content", content)
            }
            
            # Create metadata
            metadata = {
                "content_type": content_type,
                "safety_level": safety_level,
                "content_length": len(content),
                "word_count": len(content.split()),
                "violation_count": len(moderation_result["violations"]),
                "user_tier": context.user_tier
            }
            
            return self._create_response(
                success=True,
                data=response_data,
                metadata=metadata,
                execution_time_ms=execution_time_ms
            )
            
        except Exception as e:
            self._update_error()
            execution_time_ms = int((time.time() - start_time) * 1000)
            return self._create_response(
                success=False,
                data={"error": str(e)},
                metadata={"error_type": "processing_error"},
                execution_time_ms=execution_time_ms
            )
    
    def _moderate_content(self, content: str, content_type: str, safety_level: str) -> Dict[str, Any]:
        """Perform content moderation analysis"""
        violations = []
        safety_score = 100  # Start with perfect score
        
        # Check for inappropriate keywords
        content_lower = content.lower()
        for keyword in self.inappropriate_keywords:
            if keyword in content_lower:
                violations.append({
                    "type": "inappropriate_keyword",
                    "keyword": keyword,
                    "severity": "medium"
                })
                safety_score -= 10
        
        # Check for safety patterns
        for pattern in self.safety_patterns:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            if matches:
                violations.append({
                    "type": "safety_pattern",
                    "pattern": pattern,
                    "matches": matches,
                    "severity": "high"
                })
                safety_score -= 15
        
        # Content quality checks
        if len(content.split()) < 10:
            violations.append({
                "type": "content_quality",
                "issue": "content_too_short",
                "severity": "low"
            })
            safety_score -= 5
        
        # Determine if content is safe
        is_safe = safety_score >= 70 and len([v for v in violations if v["severity"] == "high"]) == 0
        
        # Generate recommendations
        recommendations = []
        if not is_safe:
            recommendations.append("Content requires review before publication")
        if safety_score < 90:
            recommendations.append("Consider revising content for better safety score")
        if len(violations) > 0:
            recommendations.append("Address identified content violations")
        
        return {
            "is_safe": is_safe,
            "safety_score": max(0, safety_score),
            "violations": violations,
            "recommendations": recommendations
        }
