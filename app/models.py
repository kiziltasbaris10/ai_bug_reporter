from pydantic import BaseModel

class BugReport(BaseModel):
    title: str
    description: str
    steps_to_reproduce: str
    expected_outcome: str
    actual_outcome: str
    priority: str
    error_type: str
    analysis_method: str = "ai_agent"
    confidence_score: float = 1.0
