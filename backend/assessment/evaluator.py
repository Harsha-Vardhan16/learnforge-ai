from typing import Dict, Any, Tuple
from backend.assessment.question_generator import get_question_by_id

def evaluate_student_answer(question_id: str, selected_answer: str) -> Tuple[bool, str, str, str]:
    """
    Evaluates whether the student's answer is correct.
    Returns: (is_correct, expected_answer, explanation, misconception_detected)
    """
    question = get_question_by_id(question_id)
    if not question:
        return False, "", "Question not found.", "Unknown"

    expected = question["expected_answer"].strip()
    user_ans = selected_answer.strip()

    # Exact match or normalized case-insensitive match
    is_correct = (expected.lower() == user_ans.lower())

    # If user selected an option letter or number like "A", "1", match against options list
    options = question.get("options", [])
    if not is_correct and options:
        # Check if user entered "A", "B", "C", "D"
        letter_map = {"A": 0, "B": 1, "C": 2, "D": 3, "0": 0, "1": 1, "2": 2, "3": 3}
        if user_ans.upper() in letter_map:
            idx = letter_map[user_ans.upper()]
            if 0 <= idx < len(options) and options[idx].lower() == expected.lower():
                is_correct = True

    misconception = None
    if not is_correct:
        misconception = question.get("misconception", "Incomplete conceptual understanding of edge case or termination criteria.")

    explanation = question.get("explanation", "")
    return is_correct, expected, explanation, misconception or ""
