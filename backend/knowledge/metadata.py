from typing import Dict, Any, Optional

def format_citation_chip(chunk: Dict[str, Any]) -> str:
    """
    Returns clean, professional citation chip text matching the specification:
    - Textbook: 'Textbook · p.42'
    - Lecture: 'Lecture · 12:34'
    - Slides: 'Slides · Slide 17'
    - Notes: 'Notes · [source_name]'
    """
    source_type = chunk.get("source_type", "document").lower()
    source_name = chunk.get("source_name", "Course Material")
    page = chunk.get("page")
    slide = chunk.get("slide")
    timestamp_display = chunk.get("timestamp_display")
    start_time = chunk.get("start_time")

    if source_type == "textbook":
        if page is not None:
            return f"Textbook · p.{page}"
        return f"Textbook · {source_name}"
    elif source_type == "slides":
        if slide is not None:
            return f"Slides · Slide {slide}"
        return f"Slides · {source_name}"
    elif source_type == "lecture":
        if timestamp_display:
            return f"Lecture · {timestamp_display}"
        elif start_time is not None:
            mins = int(start_time // 60)
            secs = int(start_time % 60)
            return f"Lecture · {mins:02d}:{secs:02d}"
        return f"Lecture · {source_name}"
    else:
        return f"Notes · {source_name}"

def extract_citation_record(chunk: Dict[str, Any], relevance_score: Optional[float] = None) -> Dict[str, Any]:
    """Generates structured citation record for API responses."""
    return {
        "source_type": chunk.get("source_type", "notes"),
        "source_name": chunk.get("source_name", "Course Material"),
        "page": chunk.get("page"),
        "slide": chunk.get("slide"),
        "start_time": chunk.get("start_time"),
        "end_time": chunk.get("end_time"),
        "timestamp_display": format_citation_chip(chunk),
        "topic": chunk.get("topic", "General"),
        "text_snippet": chunk.get("text", "")[:200] + ("..." if len(chunk.get("text", "")) > 200 else ""),
        "relevance_score": round(relevance_score, 3) if relevance_score is not None else None
    }
