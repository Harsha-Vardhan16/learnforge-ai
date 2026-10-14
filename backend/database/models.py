from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class StudentProfile(BaseModel):
    student_id: str
    name: str
    goal: str = "Concept Mastery"
    current_level: str = "Intermediate"
    created_at: str
    last_active: str

class TopicMasteryModel(BaseModel):
    student_id: str
    topic: str
    mastery: float
    attempts: int
    correct: int
    incorrect: int
    difficulty_reached: str
    last_updated: str
    status: str = "Needs Practice" # "Strong", "Competent", "Needs Practice"

class Citation(BaseModel):
    source_type: str # 'textbook', 'slides', 'lecture', 'notes'
    source_name: str
    page: Optional[int] = None
    slide: Optional[int] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    timestamp_display: Optional[str] = None
    topic: Optional[str] = None
    text_snippet: Optional[str] = None
    relevance_score: Optional[float] = None

class ChatMessageRequest(BaseModel):
    message: str
    student_id: str = "demo-student-01"
    topic: Optional[str] = None
    mode: str = "Explain" # 'Explain', 'Simplify', 'Give Example', 'Quiz Me', 'Hint', 'Challenge Me', 'Teach Differently'

class ChatMessageResponse(BaseModel):
    response: str
    topic: Optional[str] = None
    citations: List[Citation] = []
    mode: str
    suggested_followups: List[str] = []
    adaptive_strategy: Optional[str] = None # 'technical', 'analogy', 'worked_example', 'interactive_micro'
    retrieval_debug: Optional[List[Dict[str, Any]]] = None

class AssessmentGenerateRequest(BaseModel):
    topic: str
    student_id: str = "demo-student-01"
    difficulty: Optional[str] = None # If None, dynamically selected by adaptive engine

class AssessmentQuestion(BaseModel):
    question_id: str
    topic: str
    difficulty: str # 'EASY', 'MEDIUM', 'HARD'
    question_type: str # 'MCQ', 'SHORT_ANSWER', 'CODE_PREDICTION'
    prompt: str
    options: List[str] = []
    source_context: Optional[str] = None

class AssessmentSubmitRequest(BaseModel):
    student_id: str = "demo-student-01"
    question_id: str
    selected_answer: str

class AssessmentSubmitResponse(BaseModel):
    is_correct: bool
    expected_answer: str
    explanation: str
    misconception_detected: Optional[str] = None
    previous_mastery: float
    new_mastery: float
    mastery_change: float
    difficulty_reached: str
    suggested_next_action: str
    adaptive_teaching_recommendation: Optional[str] = None

class AdaptiveTeachRequest(BaseModel):
    student_id: str = "demo-student-01"
    topic: str
    attempt_count: int = 1
    concept_gap: Optional[str] = None

class AdaptiveTeachResponse(BaseModel):
    topic: str
    strategy: str # 'analogy', 'worked_example', 'interactive_micro', 'technical'
    strategy_label: str
    title: str
    content: str
    mini_question: Optional[Dict[str, Any]] = None
    citations: List[Citation] = []

class RecommendationItem(BaseModel):
    topic: str
    action_type: str # 'Strengthen Prerequisite', 'Reinforce Practice', 'Advance to Next'
    reason: str
    priority: int
    current_mastery: float
    target_concept: str

class ProgressSummary(BaseModel):
    overall_health: float
    topics: List[TopicMasteryModel]
    weak_topics: List[str]
    strong_topics: List[str]
    recommended_next: Optional[RecommendationItem] = None
    recent_attempts_count: int
    streak_days: int = 3
