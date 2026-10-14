import uuid
import re
from typing import List, Dict, Any, Optional

KNOWN_TOPICS = [
    "Binary Search",
    "Recursion",
    "Sorting",
    "Trees",
    "Arrays",
    "Linked Lists",
    "Graphs"
]

def detect_topic_from_text(text: str, default_topic: str = "General") -> str:
    """Detects most relevant DSA topic from text content using keyword frequency."""
    text_lower = text.lower()
    
    topic_keywords = {
        "Binary Search": ["binary search", "divide and conquer", "sorted array", "low high mid", "midpoint", "o(log n)"],
        "Recursion": ["recursion", "recursive", "base case", "call stack", "stack overflow", "factorial", "subproblem"],
        "Sorting": ["sort", "quicksort", "mergesort", "bubble sort", "insertion sort", "partition", "o(n log n)"],
        "Trees": ["binary tree", "bst", "node", "root", "left child", "right child", "inorder", "traversal"],
        "Arrays": ["array", "index", "elements", "contiguous", "dynamic array", "fixed size"],
        "Linked Lists": ["linked list", "singly linked", "pointer", "next node", "head node"],
        "Graphs": ["graph", "adjacency list", "dfs", "bfs", "vertex", "edges"]
    }

    best_topic = default_topic
    max_matches = 0

    for topic, keywords in topic_keywords.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        if matches > max_matches:
            max_matches = matches
            best_topic = topic

    return best_topic if max_matches > 0 else default_topic

def chunk_document_items(
    items: List[Dict[str, Any]],
    course_id: str,
    source_id: str,
    chunk_word_size: int = 150,
    overlap_words: int = 25
) -> List[Dict[str, Any]]:
    """
    Takes extracted items (pages from PDF, slides from PPTX, or cues from lecture transcript)
    and breaks them into retrieval-optimized chunks with strict metadata persistence.
    """
    chunks: List[Dict[str, Any]] = []

    for item in items:
        text = item.get("text", "").strip()
        if not text:
            continue

        words = text.split()
        source_type = item.get("source_type", "notes")
        source_name = item.get("source_name", "Course Material")
        page = item.get("page")
        slide = item.get("slide")
        start_time = item.get("start_time")
        end_time = item.get("end_time")
        timestamp_display = item.get("timestamp_display")
        
        # Determine topic
        item_topic = item.get("topic") or detect_topic_from_text(text)

        # If item is short enough, keep as single chunk
        if len(words) <= chunk_word_size + overlap_words:
            chunk_id = f"chk_{uuid.uuid4().hex[:10]}"
            chunks.append({
                "chunk_id": chunk_id,
                "source_id": source_id,
                "course_id": course_id,
                "topic": item_topic,
                "text": text,
                "source_type": source_type,
                "source_name": source_name,
                "page": page,
                "slide": slide,
                "start_time": start_time,
                "end_time": end_time,
                "timestamp_display": timestamp_display
            })
        else:
            # Sliding window chunking
            start_idx = 0
            while start_idx < len(words):
                end_idx = min(start_idx + chunk_word_size, len(words))
                sub_text = " ".join(words[start_idx:end_idx]).strip()
                sub_topic = detect_topic_from_text(sub_text, default_topic=item_topic)

                chunk_id = f"chk_{uuid.uuid4().hex[:10]}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "source_id": source_id,
                    "course_id": course_id,
                    "topic": sub_topic,
                    "text": sub_text,
                    "source_type": source_type,
                    "source_name": source_name,
                    "page": page,
                    "slide": slide,
                    "start_time": start_time,
                    "end_time": end_time,
                    "timestamp_display": timestamp_display
                })

                if end_idx >= len(words):
                    break
                start_idx += (chunk_word_size - overlap_words)

    return chunks
