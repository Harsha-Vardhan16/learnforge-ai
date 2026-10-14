import json
from fastapi import APIRouter
from typing import List, Dict, Any
from backend.database.database import get_db_connection

router = APIRouter(prefix="/course", tags=["Course & Materials"])

@router.get("/materials")
async def get_course_materials():
    """Returns list of ingested multimodal course materials and index status."""
    conn = get_db_connection()
    sources = conn.execute("""
    SELECT source_id, course_id, source_type, source_name, num_chunks, status, created_at
    FROM sources
    ORDER BY created_at DESC
    """).fetchall()

    chunks_count = conn.execute("SELECT COUNT(*) as count FROM chunks").fetchone()["count"]
    conn.close()

    materials_list = []
    for s in sources:
        materials_list.append({
            "source_id": s["source_id"],
            "course_id": s["course_id"],
            "source_type": s["source_type"],
            "source_name": s["source_name"],
            "num_chunks": s["num_chunks"],
            "status": s["status"],
            "created_at": s["created_at"]
        })

    return {
        "total_sources": len(materials_list),
        "total_chunks": chunks_count,
        "is_ready": len(materials_list) > 0,
        "materials": materials_list
    }

@router.get("/topics")
async def get_course_topics():
    """Returns the course topics and prerequisite relationships."""
    conn = get_db_connection()
    rows = conn.execute("""
    SELECT topic_id, name, order_index, parent_topic, prerequisites, description
    FROM topics
    ORDER BY order_index ASC
    """).fetchall()
    conn.close()

    topics_list = []
    for r in rows:
        prereqs = []
        try:
            prereqs = json.loads(r["prerequisites"])
        except Exception:
            pass

        topics_list.append({
            "topic_id": r["topic_id"],
            "name": r["name"],
            "order_index": r["order_index"],
            "parent_topic": r["parent_topic"],
            "prerequisites": prereqs,
            "description": r["description"]
        })

    return {
        "course_title": "Data Structures & Algorithms",
        "topics": topics_list
    }
