from fastapi import APIRouter
from backend.demo_data import seed_demo_course
from backend.student.profile import get_student_topic_analytics

router = APIRouter(prefix="/demo", tags=["Demo Mode & Evaluation"])

@router.post("/reset")
async def reset_demo_state():
    """
    Resets the demo course and student profile to the clean baseline state.
    Alex Chen: Recursion 42%, Binary Search 85%, Sorting 72%, Trees 51%.
    Ideal for repeated hackathon demonstrations and judge evaluations.
    """
    seed_demo_course(force_reset=True)
    analytics = get_student_topic_analytics("demo-student-01")
    return {
        "status": "success",
        "message": "Demo state successfully reset to initial baseline.",
        "student_id": "demo-student-01",
        "initial_health": analytics["overall_health"],
        "topics": analytics["topics"]
    }

@router.get("/status")
async def get_demo_status():
    """Returns current demo state summary."""
    analytics = get_student_topic_analytics("demo-student-01")
    return {
        "is_demo_ready": True,
        "student_id": "demo-student-01",
        "overall_health": analytics["overall_health"],
        "weak_topics": analytics["weak_topics"],
        "strong_topics": analytics["strong_topics"]
    }
