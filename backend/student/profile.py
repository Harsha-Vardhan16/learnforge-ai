from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.database.database import get_db_connection

def get_or_create_student_profile(
    student_id: str = "demo-student-01",
    name: str = "Alex Chen",
    goal: str = "Exam Preparation",
    current_level: str = "Intermediate"
) -> Dict[str, Any]:
    """Retrieves student profile or seeds initial record if missing."""
    conn = get_db_connection()
    cursor = conn.cursor()

    row = cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,)).fetchone()
    now_iso = datetime.now().isoformat()

    if row is None:
        cursor.execute("""
        INSERT INTO students (student_id, name, goal, current_level, created_at, last_active)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, name, goal, current_level, now_iso, now_iso))
        conn.commit()
        profile = {
            "student_id": student_id,
            "name": name,
            "goal": goal,
            "current_level": current_level,
            "created_at": now_iso,
            "last_active": now_iso
        }
    else:
        cursor.execute("UPDATE students SET last_active = ? WHERE student_id = ?", (now_iso, student_id))
        conn.commit()
        profile = dict(row)

    conn.close()
    return profile

def get_student_topic_analytics(student_id: str = "demo-student-01") -> Dict[str, Any]:
    """
    Computes overall learning health, categorizes strong vs weak topics,
    and returns detailed mastery metrics.
    """
    conn = get_db_connection()
    rows = conn.execute("""
    SELECT topic, mastery, attempts, correct, incorrect, difficulty_reached, last_updated
    FROM topic_mastery
    WHERE student_id = ?
    ORDER BY mastery ASC
    """, (student_id,)).fetchall()
    conn.close()

    topics = []
    strong_topics = []
    weak_topics = []
    total_mastery = 0.0

    for r in rows:
        m = float(r["mastery"])
        total_mastery += m
        status = "Needs Practice" if m < 0.60 else ("Strong" if m >= 0.75 else "Competent")

        item = {
            "student_id": student_id,
            "topic": r["topic"],
            "mastery": m,
            "attempts": int(r["attempts"]),
            "correct": int(r["correct"]),
            "incorrect": int(r["incorrect"]),
            "difficulty_reached": r["difficulty_reached"] or "EASY",
            "last_updated": r["last_updated"],
            "status": status
        }
        topics.append(item)

        if m >= 0.75:
            strong_topics.append(r["topic"])
        elif m < 0.60:
            weak_topics.append(r["topic"])

    count = len(topics)
    overall_health = round((total_mastery / count) * 100, 1) if count > 0 else 78.0

    return {
        "overall_health": overall_health,
        "topics": topics,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics
    }
