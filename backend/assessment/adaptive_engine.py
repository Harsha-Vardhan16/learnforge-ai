import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from backend.assessment.question_generator import get_questions_for_topic, get_question_by_id
from backend.assessment.evaluator import evaluate_student_answer
from backend.student.mastery import update_student_mastery_on_attempt
from backend.database.database import get_db_connection

class AdaptiveAssessmentEngine:
    def __init__(self):
        pass

    def get_adaptive_question(
        self,
        student_id: str,
        topic: str,
        difficulty_override: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Dynamically selects question difficulty based on student's current mastery.
        If mastery < 0.50: EASY
        If 0.50 <= mastery < 0.75: MEDIUM
        If mastery >= 0.75: HARD
        """
        target_diff = difficulty_override

        if not target_diff:
            conn = get_db_connection()
            row = conn.execute(
                "SELECT mastery, difficulty_reached FROM topic_mastery WHERE student_id = ? AND topic = ?",
                (student_id, topic)
            ).fetchone()
            conn.close()

            if row:
                m = float(row["mastery"])
                if m < 0.50:
                    target_diff = "EASY"
                elif m < 0.75:
                    target_diff = "MEDIUM"
                else:
                    target_diff = "HARD"
            else:
                target_diff = "MEDIUM"

        questions = get_questions_for_topic(topic, difficulty=target_diff)
        if not questions:
            questions = get_questions_for_topic(topic)

        if not questions:
            return None

        # Return first matching question
        selected = questions[0]
        return {
            "question_id": selected["question_id"],
            "topic": selected["topic"],
            "difficulty": selected["difficulty"],
            "question_type": selected["question_type"],
            "prompt": selected["prompt"],
            "options": selected.get("options", []),
            "source_context": selected.get("source_context")
        }

    def process_submission(
        self,
        student_id: str,
        question_id: str,
        selected_answer: str
    ) -> Dict[str, Any]:
        """
        Evaluates answer, records attempt in database, updates student model mastery,
        and generates personalized adaptive remediation feedback.
        """
        question = get_question_by_id(question_id)
        if not question:
            raise ValueError(f"Question {question_id} not found.")

        topic = question["topic"]
        difficulty = question["difficulty"]

        is_correct, expected, explanation, misconception = evaluate_student_answer(
            question_id=question_id,
            selected_answer=selected_answer
        )

        # Update mastery in database
        prev_mastery, new_mastery, delta = update_student_mastery_on_attempt(
            student_id=student_id,
            topic=topic,
            is_correct=is_correct,
            difficulty=difficulty
        )

        # Log attempt in SQLite
        attempt_id = f"att_{uuid.uuid4().hex[:10]}"
        now_iso = datetime.now().isoformat()
        conn = get_db_connection()
        conn.execute("""
        INSERT INTO attempts (
            attempt_id, student_id, question_id, topic, difficulty,
            selected_answer, is_correct, misconception_detected, explanation_given, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            attempt_id, student_id, question_id, topic, difficulty,
            selected_answer, 1 if is_correct else 0, misconception, explanation, now_iso
        ))
        conn.commit()
        conn.close()

        # Generate adaptive recommendation
        if is_correct:
            suggested_action = (
                f"Great job! Your {topic} mastery improved by +{int(delta * 100)}% to {int(new_mastery * 100)}%. "
                f"You are ready to advance to higher difficulty or explore connected topics."
            )
            adaptive_rec = None
        else:
            suggested_action = (
                f"Concept gap detected in {topic}. "
                f"Mastery adjusted to {int(new_mastery * 100)}% ({delta * 100:+.0f}%). "
                f"We recommend switching to an intuitive analogy and step-by-step worked example before re-testing."
            )
            adaptive_rec = (
                f"Recommended Adaptive Remediation: Learn {topic} through Strategy 2 (Real-World Analogy) "
                f"to strengthen fundamental intuition."
            )

        return {
            "is_correct": is_correct,
            "expected_answer": expected,
            "explanation": explanation,
            "misconception_detected": misconception,
            "previous_mastery": prev_mastery,
            "new_mastery": new_mastery,
            "mastery_change": delta,
            "difficulty_reached": difficulty,
            "suggested_next_action": suggested_action,
            "adaptive_teaching_recommendation": adaptive_rec
        }

_ADAPTIVE_ENGINE_INSTANCE = None

def get_adaptive_engine() -> AdaptiveAssessmentEngine:
    global _ADAPTIVE_ENGINE_INSTANCE
    if _ADAPTIVE_ENGINE_INSTANCE is None:
        _ADAPTIVE_ENGINE_INSTANCE = AdaptiveAssessmentEngine()
    return _ADAPTIVE_ENGINE_INSTANCE
