import logging
from typing import Dict, Any, List, Optional
from backend.knowledge.retriever import get_retriever
from backend.tutor.llm import get_llm_provider
from backend.tutor.prompts import BASE_SYSTEM_PROMPT, build_tutor_prompt
from backend.tutor.strategies import get_strategy_for_attempt, get_adaptive_explanation
from backend.database.database import get_db_connection
from backend.ingestion.chunker import detect_topic_from_text

logger = logging.getLogger("learnforge.tutor")

FOLLOW_UP_SUGGESTIONS = {
    "Recursion": [
        "What happens if recursion has no base case?",
        "Can you trace factorial(3) for me?",
        "How is recursion related to the Call Stack?",
        "Test me on recursion"
    ],
    "Binary Search": [
        "Why must the array be sorted for binary search?",
        "What is the time complexity of binary search?",
        "How do I prevent integer overflow in mid calculation?",
        "Test me on binary search"
    ],
    "Sorting": [
        "What is the difference between Merge Sort and Quick Sort?",
        "Why is Merge Sort stable?",
        "Explain Quick Sort partitioning",
        "Test me on sorting"
    ],
    "Trees": [
        "What is the difference between a Binary Tree and a BST?",
        "Explain Inorder traversal of a BST",
        "What is tree height vs tree depth?",
        "Test me on trees"
    ],
    "General": [
        "Explain this with a simple analogy",
        "Give me a concrete code example",
        "Test me on this topic",
        "Teach me differently"
    ]
}

class TutorService:
    def __init__(self):
        self.retriever = get_retriever()
        self.llm = get_llm_provider()

    def get_student_topic_mastery(self, student_id: str, topic: str) -> Optional[float]:
        try:
            conn = get_db_connection()
            row = conn.execute(
                "SELECT mastery FROM topic_mastery WHERE student_id = ? AND topic = ?",
                (student_id, topic)
            ).fetchone()
            conn.close()
            if row:
                return float(row["mastery"])
        except Exception as e:
            logger.warning(f"Could not load mastery: {e}")
        return None

    def process_chat(
        self,
        message: str,
        student_id: str = "demo-student-01",
        topic: Optional[str] = None,
        mode: str = "Explain"
    ) -> Dict[str, Any]:
        """
        Orchestrates grounded RAG tutoring, citation extraction,
        adaptive strategy selection, and follow-up generation.
        """
        detected_topic = topic or detect_topic_from_text(message, default_topic="Recursion")
        student_mastery = self.get_student_topic_mastery(student_id, detected_topic)

        # Check if student explicitly triggered "Teach Differently"
        msg_lower = message.lower().strip()
        is_teach_differently = (
            mode == "Teach Differently" or
            "differently" in msg_lower or
            "don't understand" in msg_lower or
            "dont understand" in msg_lower or
            "still confused" in msg_lower
        )

        # Retrieve relevant course chunks
        citations, debug_info, context_text = self.retriever.retrieve(
            query=message,
            topic=detected_topic,
            top_k=3
        )

        adaptive_strategy = None

        if is_teach_differently:
            # Provide high-impact multi-part adaptive explanation (Analogy + Visual Steps + Micro-check)
            mode = "Teach Differently"
            adaptive_info = get_adaptive_explanation(detected_topic, "analogy")
            adaptive_strategy = "analogy"
            
            response_text = (
                f"### Let's look at {detected_topic} from a completely different angle! 💡\n\n"
                f"{adaptive_info['content']}\n\n"
                f"---\n"
                f"**Key takeaway**: When learning {detected_topic}, visualize the state transitions before jumping into the code syntax. "
                f"Would you like to try a quick one-step practice to lock this in?"
            )
        else:
            # Build grounded RAG prompt
            prompt = build_tutor_prompt(
                user_message=message,
                context_text=context_text,
                mode=mode,
                student_mastery=student_mastery,
                topic=detected_topic
            )

            try:
                response_text = self.llm.generate(prompt=prompt, system_prompt=BASE_SYSTEM_PROMPT)
            except Exception as e:
                logger.error(f"LLM generation failed: {e}. Using grounded fallback.")
                from backend.tutor.llm import DeterministicEducationalProvider
                fallback_prov = DeterministicEducationalProvider()
                response_text = fallback_prov.generate(message)

        # Generate contextual follow-up prompts
        followups = FOLLOW_UP_SUGGESTIONS.get(detected_topic, FOLLOW_UP_SUGGESTIONS["General"])

        return {
            "response": response_text,
            "topic": detected_topic,
            "citations": citations,
            "mode": mode,
            "suggested_followups": followups,
            "adaptive_strategy": adaptive_strategy,
            "retrieval_debug": debug_info
        }

_TUTOR_SERVICE_INSTANCE = None

def get_tutor_service() -> TutorService:
    global _TUTOR_SERVICE_INSTANCE
    if _TUTOR_SERVICE_INSTANCE is None:
        _TUTOR_SERVICE_INSTANCE = TutorService()
    return _TUTOR_SERVICE_INSTANCE
