from fastapi import APIRouter, HTTPException
from backend.database.models import (
    AssessmentGenerateRequest,
    AssessmentQuestion,
    AssessmentSubmitRequest,
    AssessmentSubmitResponse,
    AdaptiveTeachRequest,
    AdaptiveTeachResponse
)
from backend.assessment.adaptive_engine import get_adaptive_engine
from backend.tutor.strategies import get_adaptive_explanation

router = APIRouter(prefix="/assessment", tags=["Adaptive Assessment"])

@router.post("/generate", response_model=AssessmentQuestion)
async def generate_assessment(request: AssessmentGenerateRequest):
    """Generates an assessment question adaptively calibrated to student mastery."""
    engine = get_adaptive_engine()
    question = engine.get_adaptive_question(
        student_id=request.student_id,
        topic=request.topic,
        difficulty_override=request.difficulty
    )
    if not question:
        raise HTTPException(
            status_code=404,
            detail=f"No questions found for topic '{request.topic}'"
        )
    return AssessmentQuestion(**question)

@router.post("/submit", response_model=AssessmentSubmitResponse)
async def submit_assessment(request: AssessmentSubmitRequest):
    """
    Submits a student's answer, recalculates explainable topic mastery,
    and returns immediate adaptive remediation suggestions.
    """
    try:
        engine = get_adaptive_engine()
        result = engine.process_submission(
            student_id=request.student_id,
            question_id=request.question_id,
            selected_answer=request.selected_answer
        )
        return AssessmentSubmitResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@router.post("/teach-differently", response_model=AdaptiveTeachResponse)
async def teach_differently_breakdown(request: AdaptiveTeachRequest):
    """
    Delivers targeted multi-strategy pedagogical breakdown (analogy, worked example, or micro-check)
    when a student struggles with a specific concept gap.
    """
    # Select strategy: attempt 1: technical, 2: analogy, 3: worked_example, 4: interactive_micro
    if request.attempt_count <= 1:
        strategy = "analogy" # Direct pivot to analogy on struggle
    elif request.attempt_count == 2:
        strategy = "worked_example"
    else:
        strategy = "interactive_micro"

    explanation = get_adaptive_explanation(request.topic, strategy)
    return AdaptiveTeachResponse(
        topic=request.topic,
        strategy=strategy,
        strategy_label=explanation["strategy_label"],
        title=explanation["title"],
        content=explanation["content"],
        mini_question=explanation.get("mini_question"),
        citations=[]
    )
