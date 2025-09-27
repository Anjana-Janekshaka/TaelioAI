import time
import re
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentContext, AgentResponse

class QualityAssuranceAgent(BaseAgent):
    """Agent specialized in quality assurance and story validation"""
    
    def __init__(self):
        super().__init__(
            agent_id="qa_001",
            agent_type="quality_assurance",
            name="Quality Assurance Agent",
            description="Ensures story quality, coherence, and completeness"
        )
        self.status = "ready"
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for quality assurance"""
        required_fields = ["story"]
        return all(field in input_data for field in required_fields)
    
    def get_capabilities(self) -> list:
        return [
            "story_quality_assessment",
            "coherence_checking",
            "completeness_verification",
            "grammar_validation",
            "structure_analysis",
            "quality_scoring"
        ]
    
    def get_requirements(self) -> list:
        return [
            "story_content",
            "optional_story_metadata",
            "optional_quality_standards"
        ]
    
    async def process(self, input_data: Dict[str, Any], context: AgentContext) -> AgentResponse:
        """Perform quality assurance on the story"""
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
            
            story = input_data["story"]
            story_metadata = input_data.get("story_metadata", {})
            quality_standards = input_data.get("quality_standards", "standard")
            
            # Perform quality assurance checks
            qa_result = self._assess_quality(story, story_metadata, quality_standards)
            
            # Update usage statistics
            self._update_usage()
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Create response data
            response_data = {
                "quality_score": qa_result["quality_score"],
                "is_approved": qa_result["is_approved"],
                "issues": qa_result["issues"],
                "recommendations": qa_result["recommendations"],
                "quality_metrics": qa_result["quality_metrics"]
            }
            
            # Create metadata
            metadata = {
                "story_length": len(story),
                "word_count": len(story.split()),
                "sentence_count": len(re.findall(r'[.!?]+', story)),
                "quality_standards": quality_standards,
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
    
    def _assess_quality(self, story: str, story_metadata: Dict[str, Any], quality_standards: str) -> Dict[str, Any]:
        """Assess story quality based on various metrics"""
        issues = []
        quality_score = 100  # Start with perfect score
        
        # Basic quality metrics
        word_count = len(story.split())
        sentence_count = len(re.findall(r'[.!?]+', story))
        paragraph_count = len([p for p in story.split('\n\n') if p.strip()])
        
        # Word count check
        if word_count < 100:
            issues.append({
                "type": "length",
                "issue": "story_too_short",
                "severity": "medium",
                "details": f"Story has only {word_count} words"
            })
            quality_score -= 20
        elif word_count > 5000:
            issues.append({
                "type": "length",
                "issue": "story_too_long",
                "severity": "low",
                "details": f"Story has {word_count} words"
            })
            quality_score -= 5
        
        # Sentence structure check
        if sentence_count < 5:
            issues.append({
                "type": "structure",
                "issue": "insufficient_sentences",
                "severity": "medium",
                "details": f"Story has only {sentence_count} sentences"
            })
            quality_score -= 15
        
        # Paragraph structure check
        if paragraph_count < 2:
            issues.append({
                "type": "structure",
                "issue": "insufficient_paragraphs",
                "severity": "low",
                "details": f"Story has only {paragraph_count} paragraphs"
            })
            quality_score -= 10
        
        # Grammar and punctuation check
        grammar_issues = self._check_grammar(story)
        if grammar_issues:
            issues.extend(grammar_issues)
            quality_score -= len(grammar_issues) * 5
        
        # Coherence check
        coherence_issues = self._check_coherence(story)
        if coherence_issues:
            issues.extend(coherence_issues)
            quality_score -= len(coherence_issues) * 10
        
        # Generate recommendations
        recommendations = []
        if quality_score < 80:
            recommendations.append("Story needs improvement before publication")
        if word_count < 200:
            recommendations.append("Consider expanding the story with more details")
        if sentence_count < 10:
            recommendations.append("Add more sentences to improve story flow")
        if any(issue["type"] == "grammar" for issue in issues):
            recommendations.append("Review and fix grammar issues")
        if any(issue["type"] == "coherence" for issue in issues):
            recommendations.append("Improve story coherence and flow")
        
        # Determine approval status
        is_approved = quality_score >= 70 and len([i for i in issues if i["severity"] == "high"]) == 0
        
        # Quality metrics
        quality_metrics = {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "average_sentence_length": word_count / sentence_count if sentence_count > 0 else 0,
            "readability_score": self._calculate_readability(story)
        }
        
        return {
            "quality_score": max(0, quality_score),
            "is_approved": is_approved,
            "issues": issues,
            "recommendations": recommendations,
            "quality_metrics": quality_metrics
        }
    
    def _check_grammar(self, story: str) -> List[Dict[str, Any]]:
        """Basic grammar checking"""
        issues = []
        
        # Check for common grammar issues
        if re.search(r'\bi\b', story) and not re.search(r'\bI\b', story):
            issues.append({
                "type": "grammar",
                "issue": "lowercase_i",
                "severity": "low",
                "details": "Found lowercase 'i' that should be uppercase"
            })
        
        # Check for double spaces
        if '  ' in story:
            issues.append({
                "type": "grammar",
                "issue": "double_spaces",
                "severity": "low",
                "details": "Found double spaces in text"
            })
        
        return issues
    
    def _check_coherence(self, story: str) -> List[Dict[str, Any]]:
        """Basic coherence checking"""
        issues = []
        
        # Check for abrupt transitions
        abrupt_transitions = ['suddenly', 'all of a sudden', 'out of nowhere']
        for transition in abrupt_transitions:
            if transition in story.lower():
                issues.append({
                    "type": "coherence",
                    "issue": "abrupt_transition",
                    "severity": "low",
                    "details": f"Found abrupt transition: '{transition}'"
                })
        
        return issues
    
    def _calculate_readability(self, story: str) -> float:
        """Calculate basic readability score"""
        sentences = re.findall(r'[.!?]+', story)
        words = story.split()
        
        if not sentences or not words:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Simple readability formula
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_word_length)
        return max(0, min(100, readability))
