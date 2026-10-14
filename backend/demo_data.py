import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from backend.config import DATA_DIR, DEMO_DIR, DEFAULT_STUDENT_ID
from backend.database.database import get_db_connection, init_db
from backend.ingestion.chunker import chunk_document_items
from backend.knowledge.embeddings import get_embedder
from backend.knowledge.vector_store import get_vector_store

DEMO_COURSE_ID = "course-dsa-101"

# Realistic course content with exact pages, slides, and lecture timestamps
DEMO_TEXTBOOK_ITEMS = [
    {
        "source_type": "textbook",
        "source_name": "Data Structures & Algorithm Analysis",
        "page": 42,
        "topic": "Binary Search",
        "text": (
            "Binary Search is a divide-and-conquer algorithm designed for sorted arrays. "
            "Given a target element T, the algorithm compares T with the median element of the array. "
            "If T equals the median, the index is returned immediately. If T is less than the median, "
            "the search continues in the left subarray by setting high = mid - 1. If T is greater, "
            "the search continues in the right subarray by setting low = mid + 1. "
            "Because the search interval is halved at each step, Binary Search achieves an optimal time complexity of O(log n)."
        )
    },
    {
        "source_type": "textbook",
        "source_name": "Data Structures & Algorithm Analysis",
        "page": 58,
        "topic": "Recursion",
        "text": (
            "Recursion is a programming technique in which a method invokes itself directly or indirectly. "
            "A well-formed recursive algorithm must satisfy two fundamental requirements: "
            "First, it must include one or more base cases that resolve without recursive calls. "
            "Second, every recursive invocation must make progress toward a base case. "
            "Without a valid base case, recursive calls consume stack frames until the thread exhausts its memory limit, "
            "resulting in a fatal StackOverflowError."
        )
    },
    {
        "source_type": "textbook",
        "source_name": "Data Structures & Algorithm Analysis",
        "page": 76,
        "topic": "Sorting",
        "text": (
            "Merge Sort is an asymptotically optimal comparison-based sorting algorithm. "
            "It operates by recursively splitting an array of size n into two halves of size n/2, "
            "sorting each half recursively, and then merging the two sorted halves into a single sorted array. "
            "The recurrence relation is T(n) = 2T(n/2) + O(n). By the Master Theorem, Merge Sort guarantees "
            "O(n log n) time complexity in the best, average, and worst cases."
        )
    },
    {
        "source_type": "textbook",
        "source_name": "Data Structures & Algorithm Analysis",
        "page": 94,
        "topic": "Trees",
        "text": (
            "A Binary Search Tree (BST) is a hierarchical node-based data structure where each node has at most two children. "
            "It maintains the binary search invariant: for any node N, all values in its left subtree are strictly less than N.val, "
            "and all values in its right subtree are strictly greater than N.val. "
            "Inorder traversal (Left, Root, Right) of a BST visits the nodes in sorted ascending sequence."
        )
    }
]

DEMO_SLIDES_ITEMS = [
    {
        "source_type": "slides",
        "source_name": "Searching Algorithms Slides",
        "slide": 12,
        "topic": "Binary Search",
        "text": (
            "Slide 12: Binary Search Invariants. "
            "Initial setup: low = 0, high = len(arr) - 1. Loop condition: while low <= high. "
            "Invariant: If the target exists in the array, it must reside in arr[low..high]. "
            "If low exceeds high, the search terminates with not found (-1)."
        )
    },
    {
        "source_type": "slides",
        "source_name": "Searching Algorithms Slides",
        "slide": 17,
        "topic": "Binary Search",
        "text": (
            "Slide 17: Midpoint Calculation and Integer Overflow. "
            "In languages with fixed-width 32-bit integers, calculating mid as (low + high) // 2 "
            "can trigger an integer overflow when low + high exceeds 2,147,483,647. "
            "The safe implementation is mid = low + (high - low) // 2."
        )
    },
    {
        "source_type": "slides",
        "source_name": "Recursion & Trees Masterclass",
        "slide": 8,
        "topic": "Recursion",
        "text": (
            "Slide 8: Anatomy of a Recursive Function. "
            "Every recursive function consists of: "
            "1. Base Case: The condition that terminates the recursion. "
            "2. Recursive Step: Transforming the input toward the base case. "
            "Example: factorial(n) = 1 if n <= 1 else n * factorial(n - 1)."
        )
    },
    {
        "source_type": "slides",
        "source_name": "Recursion & Trees Masterclass",
        "slide": 22,
        "topic": "Trees",
        "text": (
            "Slide 22: Tree Traversals with Recursion. "
            "Depth-First Search traversals leverage the call stack naturally: "
            "Preorder: Root -> Left -> Right. "
            "Inorder: Left -> Root -> Right (produces sorted order in BST). "
            "Postorder: Left -> Right -> Root (used for bottom-up subtree deletion)."
        )
    }
]

DEMO_LECTURE_ITEMS = [
    {
        "source_type": "lecture",
        "source_name": "DSA Lecture 3: Recursion and Trees",
        "start_time": 754.0, # 12:34
        "end_time": 789.0,
        "timestamp_display": "12:34",
        "topic": "Recursion",
        "text": (
            "Welcome back everyone. Today we are diving into recursion. "
            "Notice how the call stack works. When a function calls itself, Python or Java pushes a new activation frame. "
            "If your base case is missing, those frames keep piling up until memory runs out. "
            "That is what we call stack overflow. Always write and test your base case first."
        )
    },
    {
        "source_type": "lecture",
        "source_name": "DSA Lecture 3: Recursion and Trees",
        "start_time": 1420.0, # 23:40
        "end_time": 1465.0,
        "timestamp_display": "23:40",
        "topic": "Recursion",
        "text": (
            "Let's trace factorial of 4 on the chalkboard. "
            "factorial(4) needs factorial(3), which needs factorial(2), which needs factorial(1). "
            "At factorial(1), we finally hit the base case: return 1. "
            "Now the stack unwinds! 2 times 1 is 2, 3 times 2 is 6, 4 times 6 is 24. "
            "The base case is what enables the unwinding."
        )
    },
    {
        "source_type": "lecture",
        "source_name": "DSA Lecture 3: Recursion and Trees",
        "start_time": 1934.0, # 32:14
        "end_time": 1978.0,
        "timestamp_display": "32:14",
        "topic": "Trees",
        "text": (
            "Moving on to Binary Search Trees. Look at how recursion makes tree traversals elegant. "
            "To do an Inorder traversal, you visit the left child recursively, then print the root node, "
            "then visit the right child recursively. "
            "Because of the BST invariant where smaller keys sit on the left and larger keys on the right, "
            "Inorder traversal prints every key in ascending sorted order."
        )
    }
]

def seed_demo_course(force_reset: bool = False):
    """
    Seeds the complete demo course, topics, multimodal chunks, FAISS vector index,
    and demo student profile into the system.
    """
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if demo already seeded
    existing_chunks = cursor.execute("SELECT COUNT(*) as cnt FROM chunks WHERE course_id = ?", (DEMO_COURSE_ID,)).fetchone()
    if existing_chunks and existing_chunks["cnt"] > 0 and not force_reset:
        conn.close()
        return

    now_iso = datetime.now().isoformat()

    # 1. Seed Course
    cursor.execute("""
    INSERT OR REPLACE INTO courses (course_id, title, description, created_at)
    VALUES (?, ?, ?, ?)
    """, (
        DEMO_COURSE_ID,
        "Data Structures & Algorithms",
        "Comprehensive course covering search, sort, recursion, and tree hierarchies.",
        now_iso
    ))

    # 2. Seed Topics
    topics_seed = [
        ("top-01", "Arrays", 1, None, "[]", "Linear sequential memory collections."),
        ("top-02", "Binary Search", 2, "Arrays", '["Arrays"]', "Logarithmic search on sorted arrays."),
        ("top-03", "Sorting", 3, "Arrays", '["Arrays"]', "Comparison-based ordering algorithms."),
        ("top-04", "Recursion", 4, "Arrays", '["Arrays"]', "Self-referencing function decomposition and call stack."),
        ("top-05", "Trees", 5, "Recursion", '["Recursion"]', "Hierarchical node data structures and traversals.")
    ]
    for tid, name, order, parent, prereq, desc in topics_seed:
        cursor.execute("""
        INSERT OR REPLACE INTO topics (topic_id, course_id, name, order_index, parent_topic, prerequisites, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tid, DEMO_COURSE_ID, name, order, parent, prereq, desc))

    # 3. Seed Sources
    sources_seed = [
        ("src-01", "textbook", "Data Structures & Algorithm Analysis", "data/demo/dsa_textbook.pdf", 4),
        ("src-02", "slides", "Searching Algorithms Slides", "data/demo/searching_slides.pptx", 4),
        ("src-03", "lecture", "DSA Lecture 3: Recursion and Trees", "data/demo/dsa_lecture_03.vtt", 3)
    ]
    for sid, stype, sname, fpath, num_chk in sources_seed:
        cursor.execute("""
        INSERT OR REPLACE INTO sources (source_id, course_id, source_type, source_name, file_path, num_chunks, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid, DEMO_COURSE_ID, stype, sname, fpath, num_chk, "processed", now_iso))

    # 4. Create and Index Chunks
    all_items = DEMO_TEXTBOOK_ITEMS + DEMO_SLIDES_ITEMS + DEMO_LECTURE_ITEMS
    chunks = chunk_document_items(all_items, course_id=DEMO_COURSE_ID, source_id="src-demo", chunk_word_size=200)

    # Clean previous demo chunks from DB
    cursor.execute("DELETE FROM chunks WHERE course_id = ?", (DEMO_COURSE_ID,))

    for c in chunks:
        cursor.execute("""
        INSERT INTO chunks (chunk_id, source_id, course_id, topic, text, source_type, source_name, page, slide, start_time, end_time, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["chunk_id"], c["source_id"], c["course_id"], c["topic"], c["text"],
            c["source_type"], c["source_name"], c.get("page"), c.get("slide"),
            c.get("start_time"), c.get("end_time"), now_iso
        ))

    # 5. Seed Student Profile
    cursor.execute("""
    INSERT OR REPLACE INTO students (student_id, name, goal, current_level, created_at, last_active)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        DEFAULT_STUDENT_ID,
        "Alex Chen",
        "Exam Preparation",
        "Intermediate",
        now_iso,
        now_iso
    ))

    # 6. Seed Student Mastery Profile (Matching Master Specification!)
    # Binary Search: 85%
    # Sorting: 72%
    # Recursion: 42% (Needs Attention / Weak)
    # Trees: 51% (Needs Attention)
    mastery_seed = [
        (DEFAULT_STUDENT_ID, "Binary Search", 0.85, 8, 7, 1, "MEDIUM"),
        (DEFAULT_STUDENT_ID, "Sorting", 0.72, 6, 4, 2, "MEDIUM"),
        (DEFAULT_STUDENT_ID, "Recursion", 0.42, 7, 3, 4, "EASY"),
        (DEFAULT_STUDENT_ID, "Trees", 0.51, 5, 2, 3, "EASY"),
        (DEFAULT_STUDENT_ID, "Arrays", 0.90, 10, 9, 1, "HARD")
    ]
    for sid, top, m, att, corr, incorr, diff in mastery_seed:
        cursor.execute("""
        INSERT OR REPLACE INTO topic_mastery (student_id, topic, mastery, attempts, correct, incorrect, difficulty_reached, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (sid, top, m, att, corr, incorr, diff, now_iso))

    conn.commit()
    conn.close()

    # 7. Embed chunks and save FAISS vector store
    embedder = get_embedder()
    vector_store = get_vector_store()
    vector_store.clear()

    texts_to_embed = [c["text"] for c in chunks]
    embeddings = embedder.encode(texts_to_embed)
    vector_store.add_chunks(chunks, embeddings)
    vector_store.save()

    print(f"Successfully seeded demo course with {len(chunks)} multimodal chunks and indexed in vector store.")

if __name__ == "__main__":
    seed_demo_course(force_reset=True)
