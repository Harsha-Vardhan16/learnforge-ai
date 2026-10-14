from fastapi import APIRouter, HTTPException
from backend.database.models import ChatMessageRequest, ChatMessageResponse, Citation
from backend.tutor.tutor import get_tutor_service

router = APIRouter(prefix="", tags=["Chat & Tutor"])

@router.post("/chat", response_model=ChatMessageResponse)
async def chat_with_tutor(request: ChatMessageRequest):
    """
    Handles student chat with the AI tutor.
    Retrieves grounded context from course sources, cites exact pages/slides/timestamps,
    and tailors the teaching mode.
    """
    try:
        tutor = get_tutor_service()
        result = tutor.process_chat(
            message=request.message,
            student_id=request.student_id,
            topic=request.topic,
            mode=request.mode
        )
        return ChatMessageResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tutor error: {str(e)}")

@router.post("/tutor/explain-differently", response_model=ChatMessageResponse)
async def explain_differently(request: ChatMessageRequest):
    """Explicitly triggers Strategy 2/3 (Analogy + Worked Example) for confused students."""
    request.mode = "Teach Differently"
    return await chat_with_tutor(request)

@router.post("/tutor/hint", response_model=ChatMessageResponse)
async def get_tutor_hint(request: ChatMessageRequest):
    """Provides progressive hints without revealing the full answer."""
    request.mode = "Hint"
    return await chat_with_tutor(request)
