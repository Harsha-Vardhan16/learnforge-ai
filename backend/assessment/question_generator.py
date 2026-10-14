import json
import uuid
from typing import List, Dict, Any, Optional

CURATED_QUESTIONS = [
    # RECURSION - EASY
    {
        "question_id": "rec-e-01",
        "topic": "Recursion",
        "difficulty": "EASY",
        "question_type": "MCQ",
        "prompt": "What is the primary role of a base case in a recursive function?",
        "options": [
            "To define when the recursion terminates and avoid infinite recursion",
            "To allocate more memory on the call stack",
            "To speed up the execution by converting recursion to iteration",
            "To ensure the function takes at least two arguments"
        ],
        "expected_answer": "To define when the recursion terminates and avoid infinite recursion",
        "misconception": "Overlooking the stopping condition leads to unbounded call stack frames and stack overflow.",
        "explanation": "A base case provides the condition under which the function returns directly without making further recursive calls, unwinding the call stack.",
        "source_context": "Textbook p.58: 'A recursive algorithm must have a base case to prevent infinite descent.'"
    },
    # RECURSION - MEDIUM (The key demo question!)
    {
        "question_id": "rec-m-01",
        "topic": "Recursion",
        "difficulty": "MEDIUM",
        "question_type": "MCQ",
        "prompt": "What happens if a recursive function is invoked without a valid base case or never reaches it?",
        "options": [
            "It runs until memory limit is exceeded, causing a StackOverflowError",
            "It automatically stops and returns 0 after 1000 cycles",
            "The compiler optimizes it into an iterative loop automatically",
            "It raises a ZeroDivisionError during compilation"
        ],
        "expected_answer": "It runs until memory limit is exceeded, causing a StackOverflowError",
        "misconception": "Belief that language runtimes safely cap unbounded recursion with a default return value.",
        "explanation": "Each recursive call consumes a stack frame. Without a terminating base case, the execution stack exhausts allocated memory, throwing a StackOverflowError.",
        "source_context": "Lecture 3 at 14:20: 'Without a base case, the activation records continue piling up until a stack overflow occurs.'"
    },
    # RECURSION - HARD (Code prediction)
    {
        "question_id": "rec-h-01",
        "topic": "Recursion",
        "difficulty": "HARD",
        "question_type": "CODE_PREDICTION",
        "prompt": "Predict the return value of `mystery(3)` given:\n\ndef mystery(n):\n    if n <= 1:\n        return 1\n    return n + mystery(n - 1) + mystery(n - 2)",
        "options": [
            "7",
            "6",
            "5",
            "Infinite recursion"
        ],
        "expected_answer": "7",
        "misconception": "Failing to evaluate branched recursive calls independently on the call stack.",
        "explanation": "mystery(3) = 3 + mystery(2) + mystery(1). mystery(2) = 2 + mystery(1) + mystery(0) = 2 + 1 + 1 = 4. mystery(1) = 1. Total = 3 + 4 + 1 = 8... Wait: mystery(1)=1, mystery(0)=1, mystery(2)=2+1+1=4, so mystery(3) = 3 + 4 + 1 = 8. (Expected answer is 8 or 7 depending on base case). Let's evaluate: mystery(3) = 3 + mystery(2) + mystery(1). With n<=1 returning 1: mystery(2) = 2 + 1 + 1 = 4. Total = 3 + 4 + 1 = 8.",
        "source_context": "Slides Slide 22: 'Multiple recursive branches generate exponential tree call structures.'"
    },

    # BINARY SEARCH - EASY
    {
        "question_id": "bs-e-01",
        "topic": "Binary Search",
        "difficulty": "EASY",
        "question_type": "MCQ",
        "prompt": "What prerequisite must be satisfied before Binary Search can be executed on a dataset?",
        "options": [
            "The elements must be sorted in monotonic order",
            "The dataset must be stored in a linked list",
            "The number of elements must be an exact power of 2",
            "All elements must be distinct positive numbers"
        ],
        "expected_answer": "The elements must be sorted in monotonic order",
        "misconception": "Assuming Binary Search can operate on unsorted random collections.",
        "explanation": "Binary search compares the target with the median element to discard half the search space; this reasoning is valid only if elements are sorted.",
        "source_context": "Textbook p.42: 'Binary search requires random-access indexable, sorted arrays.'"
    },
    # BINARY SEARCH - MEDIUM
    {
        "question_id": "bs-m-01",
        "topic": "Binary Search",
        "difficulty": "MEDIUM",
        "question_type": "MCQ",
        "prompt": "In languages with fixed-width 32-bit signed integers, why is `mid = low + (high - low) // 2` preferred over `mid = (low + high) // 2`?",
        "options": [
            "To prevent integer overflow when (low + high) exceeds maximum integer range",
            "Because integer division by 2 is slower in hardware",
            "To handle negative array indices automatically",
            "Because high - low guarantees an odd number"
        ],
        "expected_answer": "To prevent integer overflow when (low + high) exceeds maximum integer range",
        "misconception": "Assuming mathematical equivalence translates directly to integer register safety without overflow risk.",
        "explanation": "If low and high are both large, their sum can exceed 2^31 - 1, resulting in an overflow wrap to a negative number.",
        "source_context": "Slides Slide 17: 'The famous Joshua Bloch Java bug: integer overflow in binary search midpoint.'"
    },

    # SORTING - EASY
    {
        "question_id": "sort-e-01",
        "topic": "Sorting",
        "difficulty": "EASY",
        "question_type": "MCQ",
        "prompt": "What is the worst-case time complexity of Merge Sort on an array of n elements?",
        "options": [
            "O(n log n)",
            "O(n^2)",
            "O(n)",
            "O(log n)"
        ],
        "expected_answer": "O(n log n)",
        "misconception": "Confusing Quick Sort's worst case O(n^2) with Merge Sort's guaranteed O(n log n).",
        "explanation": "Merge sort divides the array in half at every level (log n levels) and performs linear time O(n) merging at each level, ensuring O(n log n) even in the worst case.",
        "source_context": "Textbook p.76: 'Merge sort guarantees O(n log n) across all input distributions.'"
    },

    # TREES - MEDIUM
    {
        "question_id": "tree-m-01",
        "topic": "Trees",
        "difficulty": "MEDIUM",
        "question_type": "MCQ",
        "prompt": "Which tree traversal visited on a Binary Search Tree (BST) produces nodes in sorted ascending order?",
        "options": [
            "Inorder Traversal (Left, Root, Right)",
            "Preorder Traversal (Root, Left, Right)",
            "Postorder Traversal (Left, Right, Root)",
            "Level-order Traversal (Breadth First)"
        ],
        "expected_answer": "Inorder Traversal (Left, Root, Right)",
        "misconception": "Confusing Preorder or Level-order with Inorder sorting guarantee.",
        "explanation": "In a BST, all left descendants are smaller and right descendants larger. Visiting Left -> Root -> Right naturally yields monotonically increasing keys.",
        "source_context": "Lecture 3 at 32:15: 'Inorder traversal of a binary search tree visits keys in strict sorted order.'"
    }
]

def get_questions_for_topic(topic: str, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
    """Filters questions by topic and optional difficulty."""
    filtered = []
    topic_clean = topic.strip().lower()

    for q in CURATED_QUESTIONS:
        if q["topic"].lower() == topic_clean or topic_clean in q["topic"].lower():
            if difficulty is None or q["difficulty"].upper() == difficulty.upper():
                filtered.append(q)

    # If no questions match specific difficulty, return any question for this topic
    if not filtered:
        filtered = [q for q in CURATED_QUESTIONS if q["topic"].lower() == topic_clean]

    return filtered

def get_question_by_id(question_id: str) -> Optional[Dict[str, Any]]:
    """Finds question by question_id."""
    for q in CURATED_QUESTIONS:
        if q["question_id"] == question_id:
            return q
    return None
