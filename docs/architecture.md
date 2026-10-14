# LearnForge AI — System Architecture

**Tagline**: Your adaptive AI learning companion.  
**Target**: Multimodal AI Hackathon 2026 (IIT Mandi / KamandPrompt) — Personalized Tutoring & Adaptive Learning

---

## 1. High-Level Architecture Overview

LearnForge AI connects multimodal academic source ingestion, dense vector retrieval, grounded tutor generation, dynamic diagnostic assessment, and an explainable student model into a closed-loop adaptive learning engine.

```
+-------------------------------------------------------------------------+
|                         MULTIMODAL LEARNING SOURCES                     |
|    [PDF Textbooks]        [PPTX Slide Decks]     [Lecture Transcripts]  |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                            INGESTION PIPELINE                           |
|  - Page Extraction (pypdf)                                              |
|  - Slide Extraction (python-pptx)                                       |
|  - Timestamped Cue Parser (VTT/SRT/JSON)                                |
|  - Metadata Retention (source_name, page, slide, start_time, end_time)  |
|  - Topic Classifier & Overlapping Chunker                               |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         DENSE VECTOR KNOWLEDGE BASE                     |
|  - Sentence Transformers (all-MiniLM-L6-v2, 384-dim normalized)         |
|  - FAISS Vector Store (IndexFlatIP — Cosine Similarity)                 |
|  - Persistent Metadata Mapping (JSON + SQLite)                          |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                           RETRIEVAL & CITATION ENGINE                   |
|  - Query Vector Embedding                                               |
|  - Cosine Distance Nearest-Neighbor Search                              |
|  - Citation Chip Formatter ("Textbook · p.42", "Lecture · 12:34")       |
|  - Strict Zero-Hallucination Grounding Prompt Construction              |
+-------------------------------------------------------------------------+
                                    |
                  +-----------------+-----------------+
                  |                                   |
                  v                                   v
+-----------------------------------+   +---------------------------------+
|       AI TUTOR GENERATION         |   |   ADAPTIVE ASSESSMENT ENGINE    |
|  - Local LLM: Ollama (Llama 3.2)  |   |  - Dynamic Difficulty Tiering   |
|  - Pedagogical Modes (7 Modes)    |   |  - Misconception Diagnosis      |
|  - "Teach Differently" Strategies |   |  - Real-Time Attempt Logging    |
+-----------------------------------+   +---------------------------------+
                  \                                   /
                   \                                 /
                    v                               v
+-------------------------------------------------------------------------+
|                       EXPLAINABLE STUDENT MODEL                         |
|  - Mastery Formula: 0.5*Accuracy + 0.3*Difficulty + 0.2*Consistency     |
|  - Weak Concept Detection (< 60% confidence threshold)                  |
|  - Prerequisite DAG Graph (Arrays -> Search/Sort/Recursion -> Trees)    |
|  - Explainable "What to Learn Next" Recommendation Generator            |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         REACT FRONTEND CLIENT                           |
|  - Interactive Dashboard with Learning Health Gauge (78%)               |
|  - Grounded Chat with Clickable Citation Inspector                      |
|  - 7-Stage Animated Adaptive Loop Visualizer                            |
|  - Judge/Dev RAG Retrieval Inspector Drawer                             |
+-------------------------------------------------------------------------+
```

---

## 2. Multimodal Ingestion Pipeline

### A. PDF Textbooks (`backend/ingestion/pdf_loader.py`)
- Reads raw PDF streams using `pypdf.PdfReader`.
- Extracts clean text page by page.
- Attaches 1-indexed `page` numbers to ensure citations match the academic page numbering.

### B. PowerPoint Slides (`backend/ingestion/slide_loader.py`)
- Traverses slide presentations using `python-pptx.Presentation`.
- Gathers text frames, shape labels, tables, and presenter notes (`notes_slide`).
- Attaches 1-indexed `slide` numbers.

### C. Lecture Recordings & Transcripts (`backend/ingestion/transcript.py` & `video_loader.py`)
- Parses WebVTT (`.vtt`), SubRip (`.srt`), Whisper JSON, and bracketed timestamp logs (`[MM:SS]`).
- Extracts exact floating-point second intervals (`start_time`, `end_time`).
- Converts seconds to human-readable timecodes (e.g. `754s` -> `"12:34"`).

---

## 3. Grounded RAG & Vector Storage

1. **Embeddings**: Texts are encoded via `all-MiniLM-L6-v2` into 384-dimensional dense vectors. Vectors are $L_2$-normalized to enable cosine similarity computations.
2. **FAISS Vector Store**: Uses `faiss.IndexFlatIP` (Inner Product on unit vectors), guaranteeing millisecond retrieval on CPU.
3. **Citations Metadata**: Stored in synchronized disk files (`vector_store.faiss` and `metadata.json`) and relational SQLite tables.
4. **Citation Chips**: Format standardized as:
   - `Textbook · p.58`
   - `Lecture · 12:34`
   - `Slides · Slide 17`

---

## 4. Database Schema (SQLite)

- `students`: Profile, learning goal, current level, last active timestamp.
- `courses`: Master curriculum metadata.
- `topics`: Syllabus hierarchy with JSON prerequisite arrays.
- `sources`: Multimodal files, chunk counts, processing statuses.
- `chunks`: Granular text snippets with citation coordinates.
- `topic_mastery`: Student mastery decimal, attempt counts, correct/incorrect counters.
- `questions`: Curated and generated diagnostic items across difficulty tiers.
- `attempts`: Historical log of selected answers, correctness, and detected misconceptions.
- `learning_sessions`: Active guided session progression states.
