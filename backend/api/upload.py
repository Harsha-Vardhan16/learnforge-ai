import uuid
import shutil
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, Dict, Any

from backend.config import UPLOAD_DIR
from backend.database.database import get_db_connection
from backend.ingestion.pdf_loader import extract_text_from_pdf
from backend.ingestion.slide_loader import extract_text_from_pptx
from backend.ingestion.video_loader import extract_text_from_lecture
from backend.ingestion.chunker import chunk_document_items
from backend.knowledge.embeddings import get_embedder
from backend.knowledge.vector_store import get_vector_store

router = APIRouter(prefix="/upload", tags=["Multimodal Upload & Ingestion"])

DEFAULT_COURSE_ID = "course-dsa-101"

@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    source_name: Optional[str] = Form(None),
    course_id: Optional[str] = Form(DEFAULT_COURSE_ID)
):
    """Ingests a PDF textbook, extracting page-by-page text and indexing chunks."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF (.pdf)")

    source_id = f"src_{uuid.uuid4().hex[:8]}"
    save_path = UPLOAD_DIR / f"{source_id}_{file.filename}"
    
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    display_name = source_name or file.filename.rsplit(".", 1)[0].replace("_", " ").title()

    try:
        pages = extract_text_from_pdf(str(save_path), source_name=display_name)
        if not pages:
            raise HTTPException(status_code=400, detail="Could not extract readable text from PDF.")

        chunks = chunk_document_items(pages, course_id=course_id, source_id=source_id)

        # Embed & index
        embedder = get_embedder()
        vector_store = get_vector_store()
        embeddings = embedder.encode([c["text"] for c in chunks])
        vector_store.add_chunks(chunks, embeddings)

        # Save to SQLite
        now_iso = datetime.now().isoformat()
        conn = get_db_connection()
        conn.execute("""
        INSERT INTO sources (source_id, course_id, source_type, source_name, file_path, num_chunks, status, created_at)
        VALUES (?, ?, 'textbook', ?, ?, ?, 'processed', ?)
        """, (source_id, course_id, display_name, str(save_path), len(chunks), now_iso))

        for c in chunks:
            conn.execute("""
            INSERT INTO chunks (chunk_id, source_id, course_id, topic, text, source_type, source_name, page, slide, start_time, end_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c["chunk_id"], c["source_id"], c["course_id"], c["topic"], c["text"],
                c["source_type"], c["source_name"], c.get("page"), c.get("slide"),
                c.get("start_time"), c.get("end_time"), now_iso
            ))
        conn.commit()
        conn.close()

        detected_topics = list({c["topic"] for c in chunks})
        return {
            "status": "success",
            "message": f"Textbook '{display_name}' processed successfully.",
            "source_id": source_id,
            "source_type": "textbook",
            "source_name": display_name,
            "pages_processed": len(pages),
            "chunks_created": len(chunks),
            "topics_detected": detected_topics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest PDF: {str(e)}")

@router.post("/slides")
async def upload_slides(
    file: UploadFile = File(...),
    source_name: Optional[str] = Form(None),
    course_id: Optional[str] = Form(DEFAULT_COURSE_ID)
):
    """Ingests PPTX slides, extracting slide-by-slide text and indexing chunks."""
    if not (file.filename.lower().endswith(".pptx") or file.filename.lower().endswith(".ppt")):
        raise HTTPException(status_code=400, detail="Uploaded file must be a presentation (.pptx)")

    source_id = f"src_{uuid.uuid4().hex[:8]}"
    save_path = UPLOAD_DIR / f"{source_id}_{file.filename}"

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    display_name = source_name or file.filename.rsplit(".", 1)[0].replace("_", " ").title()

    try:
        slides = extract_text_from_pptx(str(save_path), source_name=display_name)
        if not slides:
            raise HTTPException(status_code=400, detail="No readable text found in presentation slides.")

        chunks = chunk_document_items(slides, course_id=course_id, source_id=source_id)

        # Embed & index
        embedder = get_embedder()
        vector_store = get_vector_store()
        embeddings = embedder.encode([c["text"] for c in chunks])
        vector_store.add_chunks(chunks, embeddings)

        # Save to SQLite
        now_iso = datetime.now().isoformat()
        conn = get_db_connection()
        conn.execute("""
        INSERT INTO sources (source_id, course_id, source_type, source_name, file_path, num_chunks, status, created_at)
        VALUES (?, ?, 'slides', ?, ?, ?, 'processed', ?)
        """, (source_id, course_id, display_name, str(save_path), len(chunks), now_iso))

        for c in chunks:
            conn.execute("""
            INSERT INTO chunks (chunk_id, source_id, course_id, topic, text, source_type, source_name, page, slide, start_time, end_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c["chunk_id"], c["source_id"], c["course_id"], c["topic"], c["text"],
                c["source_type"], c["source_name"], c.get("page"), c.get("slide"),
                c.get("start_time"), c.get("end_time"), now_iso
            ))
        conn.commit()
        conn.close()

        detected_topics = list({c["topic"] for c in chunks})
        return {
            "status": "success",
            "message": f"Presentation '{display_name}' processed successfully.",
            "source_id": source_id,
            "source_type": "slides",
            "source_name": display_name,
            "slides_processed": len(slides),
            "chunks_created": len(chunks),
            "topics_detected": detected_topics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest slides: {str(e)}")

@router.post("/video")
async def upload_video(
    file: UploadFile = File(...),
    source_name: Optional[str] = Form(None),
    course_id: Optional[str] = Form(DEFAULT_COURSE_ID)
):
    """Ingests lecture recording or timestamped transcript (.vtt, .srt, .json, .txt, .mp4)."""
    source_id = f"src_{uuid.uuid4().hex[:8]}"
    save_path = UPLOAD_DIR / f"{source_id}_{file.filename}"

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    display_name = source_name or file.filename.rsplit(".", 1)[0].replace("_", " ").title()

    try:
        cues = extract_text_from_lecture(str(save_path), source_name=display_name)
        chunks = chunk_document_items(cues, course_id=course_id, source_id=source_id)

        # Embed & index
        embedder = get_embedder()
        vector_store = get_vector_store()
        embeddings = embedder.encode([c["text"] for c in chunks])
        vector_store.add_chunks(chunks, embeddings)

        # Save to SQLite
        now_iso = datetime.now().isoformat()
        conn = get_db_connection()
        conn.execute("""
        INSERT INTO sources (source_id, course_id, source_type, source_name, file_path, num_chunks, status, created_at)
        VALUES (?, ?, 'lecture', ?, ?, ?, 'processed', ?)
        """, (source_id, course_id, display_name, str(save_path), len(chunks), now_iso))

        for c in chunks:
            conn.execute("""
            INSERT INTO chunks (chunk_id, source_id, course_id, topic, text, source_type, source_name, page, slide, start_time, end_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c["chunk_id"], c["source_id"], c["course_id"], c["topic"], c["text"],
                c["source_type"], c["source_name"], c.get("page"), c.get("slide"),
                c.get("start_time"), c.get("end_time"), now_iso
            ))
        conn.commit()
        conn.close()

        detected_topics = list({c["topic"] for c in chunks})
        return {
            "status": "success",
            "message": f"Lecture '{display_name}' processed successfully with timestamp citations.",
            "source_id": source_id,
            "source_type": "lecture",
            "source_name": display_name,
            "segments_processed": len(cues),
            "chunks_created": len(chunks),
            "topics_detected": detected_topics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest lecture: {str(e)}")
