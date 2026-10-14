import os
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL, DB_PATH
from backend.database.database import init_db, get_db_connection
from backend.demo_data import seed_demo_course
from backend.knowledge.vector_store import get_vector_store
from backend.knowledge.embeddings import get_embedder
from backend.tutor.llm import OllamaProvider

# Import API Routers
from backend.api.chat import router as chat_router
from backend.api.upload import router as upload_router
from backend.api.course import router as course_router
from backend.api.assessment import router as assessment_router
from backend.api.progress import router as progress_router
from backend.api.recommendation import router as rec_router
from backend.api.demo import router as demo_router

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("learnforge.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes database and seeds demo data on application startup."""
    logger.info("Initializing LearnForge AI backend...")
    init_db()
    try:
        # Pre-seed demo course if not already present
        seed_demo_course(force_reset=False)
        logger.info("Demo course knowledge base verified and active.")
    except Exception as e:
        logger.error(f"Error during initial seeding: {e}")
    yield
    logger.info("LearnForge AI backend shutting down.")

app = FastAPI(
    title="LearnForge AI API",
    description="Your adaptive AI learning companion. Source-grounded RAG tutoring and student mastery loop.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local React/Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(course_router)
app.include_router(assessment_router)
app.include_router(progress_router)
app.include_router(rec_router)
app.include_router(demo_router)

@app.get("/")
async def root():
    return {
        "project": "LearnForge AI",
        "tagline": "Your adaptive AI learning companion.",
        "status": "online",
        "version": "1.0.0",
        "hackathon": "Multimodal AI Hackathon 2026",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Checks Python, Ollama, Vector Store, and SQLite database connectivity."""
    # Ollama health
    ollama = OllamaProvider()
    ollama_ok = ollama.is_available()

    # Vector store count
    vector_store = get_vector_store()
    chunk_count = vector_store.count()

    # Database health
    db_ok = False
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1").fetchone()
        conn.close()
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "status": "healthy" if db_ok else "degraded",
        "components": {
            "python_runtime": sys.version.split()[0],
            "database": "connected" if db_ok else "disconnected",
            "database_file": str(DB_PATH),
            "vector_store": "ready",
            "indexed_chunks": chunk_count,
            "ollama_service": "online" if ollama_ok else "offline (using robust local fallback)",
            "ollama_model": OLLAMA_MODEL,
            "ollama_url": OLLAMA_BASE_URL
        }
    }

# Mount built React frontend if dist exists
from pathlib import Path
from fastapi.staticfiles import StaticFiles

frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    @app.get("/app")
    @app.get("/demo-ui")
    async def serve_ui():
        from fastapi.responses import FileResponse
        return FileResponse(str(frontend_dist / "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

