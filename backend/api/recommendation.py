from fastapi import APIRouter, Query
from backend.database.models import RecommendationItem
from backend.student.recommendations import generate_explainable_recommendation

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("", response_model=RecommendationItem)
async def get_recommendations(student_id: str = Query("demo-student-01")):
    """
    Returns an explainable next learning recommendation with explicit rationale,
    based on prerequisite graph, current topic mastery, and recent errors.
    """
    rec_dict = generate_explainable_recommendation(student_id=student_id)
    return RecommendationItem(**rec_dict)
