from datetime import datetime
from typing import Dict, Any, Tuple
from backend.database.database import get_db_connection

def calculate_mastery(
    recent_accuracy: float,
    difficulty_reached: str = "EASY",
    consistency_score: float = 0.5
) -> float:
    """
    Explainable Mastery Algorithm (Documented Specification):
    
    Formula:
        mastery = 0.5 * recent_accuracy + 0.3 * difficulty_adjusted_performance + 0.2 * consistency
    
    Weights:
        - recent_accuracy (50%): Student's recent correctness ratio on questions.
        - difficulty_adjusted_performance (30%): Weight of difficulty solved (EASY: 0.6, MEDIUM: 0.85, HARD: 1.0).
        - consistency_score (20%): Consistency and streak factor.
        
    Result:
        Clamped to [0.0, 1.0].
    """
    diff_map = {
        "EASY": 0.60,
        "MEDIUM": 0.85,
        "HARD": 1.00
    }
    diff_factor = diff_map.get(difficulty_reached.upper(), 0.60)

    raw_mastery = (0.50 * recent_accuracy) + (0.30 * diff_factor) + (0.20 * consistency_score)
    return round(max(0.0, min(1.0, raw_mastery)), 2)

def update_student_mastery_on_attempt(
    student_id: str,
    topic: str,
    is_correct: bool,
    difficulty: str
) -> Tuple[float, float, float]:
    """
    Updates the database with the student's new attempt and recalculates mastery.
    Returns: (previous_mastery, new_mastery, mastery_delta)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    row = cursor.execute(
        "SELECT mastery, attempts, correct, incorrect, difficulty_reached FROM topic_mastery WHERE student_id = ? AND topic = ?",
        (student_id, topic)
    ).fetchone()

    now_iso = datetime.now().isoformat()

    if row is None:
        prev_mastery = 0.40 # Initial baseline
        attempts = 0
        correct = 0
        incorrect = 0
        current_diff = difficulty
    else:
        prev_mastery = float(row["mastery"])
        attempts = int(row["attempts"])
        correct = int(row["correct"])
        incorrect = int(row["incorrect"])
        current_diff = row["difficulty_reached"] or difficulty

    attempts += 1
    if is_correct:
        correct += 1
        # Upgrade difficulty if answering correctly on medium/hard
        if difficulty == "EASY" and current_diff == "EASY":
            current_diff = "MEDIUM"
        elif difficulty == "MEDIUM":
            current_diff = "HARD"
    else:
        incorrect += 1
        # Drop difficulty target if failing
        if current_diff == "HARD":
            current_diff = "MEDIUM"
        elif current_diff == "MEDIUM":
            current_diff = "EASY"

    accuracy = correct / attempts if attempts > 0 else 0.0
    consistency = 0.8 if is_correct else 0.3

    new_mastery = calculate_mastery(
        recent_accuracy=accuracy,
        difficulty_reached=current_diff,
        consistency_score=consistency
    )

    delta = round(new_mastery - prev_mastery, 2)

    cursor.execute("""
    INSERT INTO topic_mastery (student_id, topic, mastery, attempts, correct, incorrect, difficulty_reached, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(student_id, topic) DO UPDATE SET
        mastery = excluded.mastery,
        attempts = excluded.attempts,
        correct = excluded.correct,
        incorrect = excluded.incorrect,
        difficulty_reached = excluded.difficulty_reached,
        last_updated = excluded.last_updated
    """, (student_id, topic, new_mastery, attempts, correct, incorrect, current_diff, now_iso))

    conn.commit()
    conn.close()

    return prev_mastery, new_mastery, delta
