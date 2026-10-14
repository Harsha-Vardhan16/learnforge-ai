from fastapi import APIRouter, Query
from backend.database.models import ProgressSummary, TopicMasteryModel
from backend.student.profile import get_student_topic_analytics, get_or_create_student_profile
from backend.student.recommendations import generate_explainable_recommendation
from backend.database.database import get_db_connection

router = APIRouter(prefix="/progress", tags=["Student Progress & Analytics"])

@router.get("", response_model=ProgressSummary)
async def get_student_progress(student_id: str = Query("demo-student-01")):
    """
    Returns complete progress summary:
    - Overall Learning Health percentage
    - Mastery per topic (Arrays, Binary Search, Sorting, Recursion, Trees)
    - Automatically detected Weak and Strong topics
    - Explainable Next Topic Recommendation
    """
    profile = get_or_create_student_profile(student_id=student_id)
    analytics = get_student_topic_analytics(student_id=student_id)
    rec = generate_explainable_recommendation(student_id=student_id)

    # Count recent attempts
    conn = get_db_connection()
    attempts_cnt = conn.execute(
        "SELECT COUNT(*) as cnt FROM attempts WHERE student_id = ?",
        (student_id,)
    ).fetchone()["cnt"]
    conn.close()

    topic_models = [TopicMasteryModel(**t) for t in analytics["topics"]]

    return ProgressSummary(
        overall_health=analytics["overall_health"],
        topics=topic_models,
        weak_topics=analytics["weak_topics"],
        strong_topics=analytics["strong_topics"],
        recommended_next=rec,
        recent_attempts_count=attempts_cnt,
        streak_days=3
    )

@router.get("/topics")
async def get_topic_mastery_list(student_id: str = Query("demo-student-01")):
    """Returns granular topic mastery records for the student."""
    analytics = get_student_topic_analytics(student_id=student_id)
    return {
        "student_id": student_id,
        "topics": analytics["topics"]
    }
