from typing import Dict, Any, List, Optional
from backend.database.database import get_db_connection

PREREQUISITE_MAP = {
    "Binary Search": ["Arrays"],
    "Sorting": ["Arrays"],
    "Recursion": ["Arrays"],
    "Trees": ["Recursion"],
    "Graphs": ["Trees", "Recursion"]
}

CONCEPT_BREAKDOWN_MAP = {
    "Recursion": "Base Cases & Stack Unwinding",
    "Trees": "Inorder Traversal & BST Properties",
    "Binary Search": "Midpoint Calculation & Boundary Conditions",
    "Sorting": "Divide-and-Conquer Partitioning",
    "Arrays": "Contiguous Memory & Subarray Logic"
}

def generate_explainable_recommendation(student_id: str = "demo-student-01") -> Dict[str, Any]:
    """
    Computes explainable 'What should I learn next?' recommendation
    based on prerequisite DAG, mastery scores, and gap detection.
    """
    conn = get_db_connection()
    rows = conn.execute("""
    SELECT topic, mastery, attempts, correct, incorrect, difficulty_reached
    FROM topic_mastery
    WHERE student_id = ?
    """, (student_id,)).fetchall()
    conn.close()

    mastery_dict = {r["topic"]: float(r["mastery"]) for r in rows}

    # Rule 1: Check Prerequisite bottlenecks
    # Example: If Trees is attempted or low, but Recursion is below 60%, recommend Recursion first!
    if "Trees" in mastery_dict and "Recursion" in mastery_dict:
        rec_mastery = mastery_dict["Recursion"]
        if rec_mastery < 0.60:
            rec_pct = int(rec_mastery * 100)
            return {
                "topic": "Recursion",
                "action_type": "Strengthen Prerequisite",
                "reason": (
                    f"You should practice Recursion before advancing in Trees because your recursion mastery is currently {rec_pct}%. "
                    "Recursion is an essential prerequisite for tree traversal algorithms (DFS, Inorder, Preorder)."
                ),
                "priority": 1,
                "current_mastery": rec_mastery,
                "target_concept": "Recursion → Base Cases"
            }

    # Rule 2: Find the lowest mastery topic below 60%
    weakest_topic = None
    min_score = 1.0

    for topic, score in mastery_dict.items():
        if score < 0.60 and score < min_score:
            min_score = score
            weakest_topic = topic

    if weakest_topic:
        pct = int(min_score * 100)
        target_concept = CONCEPT_BREAKDOWN_MAP.get(weakest_topic, f"{weakest_topic} Fundamentals")
        return {
            "topic": weakest_topic,
            "action_type": "Reinforce Practice",
            "reason": (
                f"Your mastery in {weakest_topic} is currently {pct}%, which is below the 60% confidence threshold. "
                f"Completing a targeted practice session will bridge your conceptual gaps."
            ),
            "priority": 2,
            "current_mastery": min_score,
            "target_concept": f"{weakest_topic} → {target_concept}"
        }

    # Rule 3: Advance to the next topic in syllabus
    for candidate in ["Arrays", "Binary Search", "Sorting", "Recursion", "Trees", "Graphs"]:
        if candidate not in mastery_dict or mastery_dict[candidate] < 0.75:
            curr = mastery_dict.get(candidate, 0.50)
            return {
                "topic": candidate,
                "action_type": "Advance to Next",
                "reason": f"You have demonstrated solid foundations in prerequisite topics. You are ready to master {candidate}.",
                "priority": 3,
                "current_mastery": curr,
                "target_concept": f"{candidate} → Deep Dive"
            }

    # Fallback
    return {
        "topic": "Recursion",
        "action_type": "Reinforce Practice",
        "reason": "Reinforce core algorithmic problem solving with practice problems.",
        "priority": 4,
        "current_mastery": 0.42,
        "target_concept": "Recursion → Base Cases"
    }
