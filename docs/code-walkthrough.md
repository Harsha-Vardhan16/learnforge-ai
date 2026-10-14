# LearnForge AI — Module-by-Module Code Walkthrough

This document takes you through every important file in the project in logical execution order so you can trace how data flows from file ingestion to vector search, tutoring, and mastery updates.

---

## 1. `backend/main.py`
- **What it does**: The FastAPI application entrypoint.
- **Key Lines**:
  - `lifespan(app)`: Initializes SQLite and auto-seeds the demo course and FAISS index on startup.
  - `app.include_router(...)`: Registers modular API routers for chat, upload, course, assessment, progress, and demo.
  - `app.get("/health")`: Reports operational health of Python, SQLite, FAISS, and Ollama.

## 2. Ingestion (`backend/ingestion/`)
- `pdf_loader.py`: Uses `pypdf.PdfReader` to extract text page-by-page. Returns records with `page` (1-indexed) and `source_type="textbook"`.
- `slide_loader.py`: Uses `pptx.Presentation` to extract slide text, shape labels, and speaker notes. Returns records with `slide` (1-indexed) and `source_type="slides"`.
- `video_loader.py` & `transcript.py`: Parses WebVTT (`.vtt`), SubRip (`.srt`), Whisper JSON, and timestamped bracketed notes (`[12:34]`). Attaches `start_time`, `end_time`, and `timestamp_display`.

## 3. Chunking (`backend/ingestion/chunker.py`)
- **What it does**: Breaks extracted pages, slides, or transcript segments into optimal retrieval chunks (~150-250 words) with overlapping boundaries.
- **Key Functions**:
  - `detect_topic_from_text(text)`: Analyzes keyword frequency to associate chunks with core syllabus topics (`Recursion`, `Binary Search`, `Sorting`, `Trees`, `Arrays`).
  - `chunk_document_items(...)`: Retains all metadata fields (`source_type`, `source_name`, `page`, `slide`, `start_time`, `end_time`) on every single chunk.

## 4. Embeddings (`backend/knowledge/embeddings.py`)
- **What it does**: Computes dense numerical representations of text.
- **Key Class**: `Embedder`
  - Loads `all-MiniLM-L6-v2` via `sentence-transformers` on CPU.
  - Encodes strings into 384-dimensional $L_2$-normalized numpy vectors.
  - Provides a deterministic offline hashing fallback if transformer weights cannot be downloaded.

## 5. FAISS Vector Store (`backend/knowledge/vector_store.py`)
- **What it does**: Performs ultra-fast nearest-neighbor similarity search.
- **Key Class**: `VectorStore`
  - Uses `faiss.IndexFlatIP(384)` (Inner Product on normalized vectors equals Cosine Similarity).
  - `add_chunks(chunks, embeddings)`: Adds vectors to the index and metadata dictionaries to memory.
  - `save()` / `load()`: Persists the index to `data/vector_store.faiss` and `data/metadata.json`.

## 6. Retrieval (`backend/knowledge/retriever.py`)
- **What it does**: Executes vector queries and formats grounded context for the LLM.
- **Key Method**: `retrieve(query, topic, top_k=3)`
  - Encodes the user's question.
  - Searches FAISS for top-3 closest chunks.
  - Formats human-readable citation chips (`Textbook · p.58`, `Lecture · 12:34`).
  - Generates debug metrics (cosine scores) for the Judge Retrieval Inspector.

## 7. LLM Integration (`backend/tutor/llm.py`)
- **What it does**: Manages local LLM inference.
- **Key Classes**:
  - `OllamaProvider`: Calls local Ollama API at `http://localhost:11434/api/generate` with model `llama3.2:latest`.
  - `DeterministicEducationalProvider`: Fallback provider that guarantees 100% reliable pedagogical answers if Ollama is paused.

## 8. Chat Pipeline (`backend/tutor/tutor.py` & `prompts.py`)
- **What it does**: Orchestrates tutor conversation, pedagogical modes, and grounded prompts.
- **Modes Supported**: Explain, Simplify, Give Example, Quiz Me, Hint, Challenge Me, Teach Differently.
- **Grounded Prompt**: Explicitly instructs the LLM to rely only on verified course chunks and avoid inventing sources.

## 9. Adaptive Assessment (`backend/assessment/`)
- `question_generator.py`: Holds diagnostic question items across difficulty levels (`EASY`, `MEDIUM`, `HARD`) and question types (MCQ, Code Prediction, Short Answer).
- `evaluator.py`: Verifies student answers and identifies specific misconceptions.
- `adaptive_engine.py`: Selects difficulty based on student mastery, logs attempts, and triggers adaptive remediation recommendations.

## 10. Student Model (`backend/student/profile.py`)
- **What it does**: Tracks student state across topics.
- Categorizes concepts into:
  - Strong Concepts ($\ge 75\%$)
  - Competent Concepts ($60\% - 74\%$)
  - Weak Concepts / Needs Attention ($< 60\%$)

## 11. Mastery Algorithm (`backend/student/mastery.py`)
- **What it does**: Calculates mastery using the documented formula:
  $$\text{mastery} = 0.50 \times \text{recent\_accuracy} + 0.30 \times \text{difficulty\_factor} + 0.20 \times \text{consistency}$$
- Updates SQLite on each attempt and returns before/after deltas.

## 12. Recommendation Engine (`backend/student/recommendations.py`)
- **What it does**: Traverses prerequisite tree (`Arrays` $\to$ `Recursion` $\to$ `Trees`).
- Warns student with explainable rationale if prerequisite mastery is low.

## 13. Frontend Client (`frontend/src/`)
- `services/api.js`: Typed API client for all backend endpoints.
- `pages/DashboardPage.jsx`: Main overview with Learning Health gauge (78%), weak topics, and Adaptive Loop visualizer.
- `pages/TutorChatPage.jsx`: Grounded tutor chat with clickable citation chips and "Teach Differently" action.
- `pages/PracticePage.jsx`: Interactive assessment runner with dynamic evaluation, misconception diagnosis, and micro-check mastery leap.
- `pages/CourseMaterialsPage.jsx`: Multimodal ingestion panel for PDF, PPTX, and lecture transcripts.
- `pages/ProgressPage.jsx`: Horizontal mastery spectrum bars and formula transparency card.

## 14. Database (`backend/database/database.py`)
- Manages local SQLite connection at `data/learnforge.db`.
- Creates 8 relational tables: `students`, `courses`, `topics`, `sources`, `chunks`, `topic_mastery`, `questions`, `attempts`, `learning_sessions`.
