# LearnForge AI

> **Tagline**: *Your adaptive AI learning companion.*  
> **Submission Target**: Multimodal AI Hackathon 2026 (IIT Mandi / KamandPrompt)  
> **Theme**: Personalized Tutoring & Adaptive Learning

---

## 1. Project Overview

**LearnForge AI** is an adaptive, source-grounded multimodal AI tutoring platform. Instead of acting as another generic "ChatGPT with PDF upload," LearnForge AI unifies textbooks, lecture slides, and lecture video transcripts into a searchable knowledge base, delivers answers with verified citations, and continuously tracks student mastery across topics.

When a student struggles with a concept, LearnForge AI does not repeat the same textbook definition. It detects the conceptual gap, dynamically switches its teaching strategy (using real-world analogies, step-by-step call stack traces, and interactive checkpoints), re-tests understanding, updates the student model, and recommends what to learn next based on course prerequisite graphs.

---

## 2. The Problem

Students prepare for rigorous exams using fragmented learning materials:
1. Thick textbook PDFs
2. Multi-deck presentation slides
3. Hours of recorded lecture videos

Standard educational AI tools suffer from critical flaws:
- **No Progress Awareness**: They answer isolated questions without understanding what the student knows or struggles with.
- **Hallucinated Citations**: They generate confident answers without verifiable references.
- **Monotone Teaching**: When a student says *"I don't get it"*, chatbots typically output the exact same formal definition using slightly different words.
- **No Prerequisite Intelligence**: They cannot identify that a student's difficulty with Tree Traversals stems from a weak understanding of Recursion Base Cases.

---

## 3. The Solution

LearnForge AI bridges this gap with an end-to-end adaptive learning system:
1. **Multimodal Ingestion**: Ingests PDFs, PPTX slides, and timestamped lecture transcripts into a unified FAISS vector knowledge base.
2. **Source-Grounded Tutoring**: Delivers answers with clickable citations (`Textbook · p.58`, `Lecture · 12:34`, `Slides · Slide 17`).
3. **Adaptive Diagnostic Engine**: Serves questions dynamically calibrated to the student's current mastery level (`EASY`, `MEDIUM`, `HARD`).
4. **Misconception Diagnosis**: Identifies specific mental blocks (e.g. *"Belief that recursion terminates at 0 without a base case"*).
5. **Teach Differently**: Pivots explanation strategies to real-world analogies, visual state flows, and micro-checks.
6. **Explainable Student Model**: Recalculates mastery using a documented, transparent mathematical formula.
7. **Prerequisite-Aware Recommendations**: Recommends the exact next learning action with pedagogical reasoning.

---

## 4. The Core Differentiator: The Adaptive Tutor Loop

```
  [1. UNDERSTAND]   ---> Student asks question; Tutor responds with verified citations.
         |
         v
    [2. TEST]       ---> System serves diagnostic check calibrated to student's level.
         |
         v
 [3. DETECT GAP]    ---> Student error triggers misconception diagnosis.
         |
         v
   [4. ADAPT]       ---> Tutor switches strategy: delivers real-world analogy & step trace.
         |
         v
  [5. REASSESS]     ---> Student solves micro-check question to confirm understanding.
         |
         v
[6. UPDATE MODEL]   ---> Mastery formula updates: 42% -> 67% (+25%).
         |
         v
 [7. RECOMMEND]     ---> System recommends next topic based on prerequisite graph.
```

> **The 30-Second Judge Takeaway**:  
> *"Most educational AI systems answer what you ask. LearnForge AI remembers what you struggle with and changes what it teaches next."*

---

## 5. Key Features

- **🏠 Command Center Dashboard**: Overall Learning Health gauge (78%), Strong Topics, Needs Practice topics, and Recommended Next cards.
- **💬 Source-Grounded AI Tutor**: 7 pedagogical modes (`Explain`, `Simplify`, `Give Example`, `Quiz Me`, `Hint`, `Challenge Me`, `Teach Differently`).
- **📚 Multimodal Source Manager**: Interactive ingestion of PDF textbooks, PPTX slides, and lecture video transcripts.
- **🎯 Dynamic Adaptive Assessment**: Calibrated questions, misconception diagnosis, and instant remediation.
- **💡 "Teach Differently" Feature**: Switches from formal definitions to intuitive mental models (Russian Nesting Dolls) and step traces (`factorial(4)`).
- **📈 Mastery Analytics & Spectrum**: Horizontal progress bars, accuracy counters, and transparent formula breakdown.
- **🔍 RAG Retrieval Inspector (Judge / Dev Mode)**: Collapsible drawer displaying raw FAISS cosine similarity scores and ground-truth text chunks.
- **⚡ 1-Click Demo Tour**: 3-minute guided walkthrough overlay built specifically for hackathon judging.

---

## 6. Architecture & Tech Stack

```
learnforge-ai/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint, lifespan seeding, route mounting
│   ├── config.py                # System paths, Ollama settings, vector store paths
│   ├── api/                     # Typed REST API endpoints (chat, upload, course, assessment, progress)
│   ├── ingestion/               # Multimodal loaders (PDF, PPTX, Video/VTT, Overlapping chunker)
│   ├── knowledge/               # Embeddings (all-MiniLM-L6-v2), FAISS vector store, retriever
│   ├── tutor/                   # Ollama Llama 3.2 provider, prompts, adaptive strategies
│   ├── assessment/              # Question generator, answer evaluator, adaptive engine
│   ├── student/                 # Profile manager, explainable mastery calculator, recommendations
│   ├── database/                # SQLite connection, schema initialization, Pydantic models
│   └── demo_data.py             # Realistic DSA demo course seeder
├── frontend/
│   ├── src/
│   │   ├── components/          # Navbar, Sidebar, AdaptiveLoop, CitationBadge, RagInspector, DemoTour
│   │   ├── pages/               # LandingPage, DashboardPage, TutorChatPage, CourseMaterialsPage, PracticePage, ProgressPage
│   │   ├── services/api.js      # Typed frontend API client abstraction
│   │   ├── App.jsx              # Application state and routing
│   │   └── index.css            # Modern dark/slate design system
│   └── package.json
├── data/
│   ├── demo/                    # Realistic sample textbook, slides, and lecture transcript
│   └── uploads/                 # Storage for user-uploaded documents
├── docs/                        # Complete architecture, learning guide, code walkthrough, demo script
└── tests/                       # 12 comprehensive unit and integration tests (100% passing)
```

### Technology Highlights
- **Backend Framework**: Python 3.11, FastAPI, Uvicorn, Pydantic v2
- **Vector Database**: FAISS (Facebook AI Similarity Search) IndexFlatIP (Cosine metric)
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`, 384 dimensions)
- **Local LLM**: Ollama (`llama3.2:latest`) with deterministic educational fallback
- **Database**: SQLite (8 relational tables)
- **Document Parsers**: `pypdf`, `python-pptx`, regex-based WebVTT/SRT transcript parser
- **Frontend**: React 19, Vite, Tailwind CSS v4, Lucide Icons, Canvas-Confetti

---

## 7. Explainable Student Mastery Algorithm

LearnForge AI avoids opaque black-box scoring by using a documented, transparent formula:

$$\text{mastery} = 0.50 \times \text{recent\_accuracy} + 0.30 \times \text{difficulty\_factor} + 0.20 \times \text{consistency}$$

- **Recent Accuracy (50%)**: Correct attempts over total attempts ($\frac{\text{correct}}{\text{attempts}}$).
- **Difficulty Factor (30%)**: Scaled reward reflecting problem complexity (`EASY: 0.60`, `MEDIUM: 0.85`, `HARD: 1.00`).
- **Consistency Score (20%)**: Cognitive retention streak multiplier.

Result is clamped to $[0.00, 1.00]$ and displayed as a percentage (e.g. $42\%$).

---

## 8. Installation & Setup (Windows)

### Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Node.js 18+ and npm
- Ollama (Optional for local LLM inference: `ollama run llama3.2`)

### 1. Clone & Enter Directory
```powershell
cd C:\Users\jhars\.gemini\antigravity\scratch\learnforge-ai
```

### 2. Backend Setup
```powershell
# Create and activate Python virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*The database and demo knowledge base automatically seed on startup!*

### 3. Frontend Setup
Open a separate PowerShell terminal:
```powershell
cd C:\Users\jhars\.gemini\antigravity\scratch\learnforge-ai\frontend
npm install
npm run dev
```

Open your browser at: **`http://localhost:5173`**

---

## 9. Running the Automated Test Suite

LearnForge AI includes 12 automated unit and integration tests covering ingestion, chunking, vector search, question evaluation, mastery formulas, and API endpoints.

```powershell
cd C:\Users\jhars\.gemini\antigravity\scratch\learnforge-ai
python -m unittest discover tests
```
**Result**: `Ran 12 tests in ~50s — OK (100% Pass Rate)`

---

## 10. The Winning Hackathon Demo Flow (3 Minutes)

1. **Start on Landing Page**: Click **"Try Demo Course"** to load the pre-indexed Data Structures & Algorithms course.
2. **Dashboard Overview**: Point to the **Learning Health (78%)**, Strong Topics (Binary Search 85%), and Needs Practice (Recursion 42%).
3. **Ask Tutor**: Navigate to **Ask Tutor** and ask *"Why does recursion need a base case?"*. Show the verified citation chips `[Textbook · p.58]` and `[Lecture · 12:34]`. Expand the **RAG Inspector** to verify raw cosine similarity.
4. **Take Diagnostic Quiz**: Go to **Practice & Quiz**. Answer the Recursion question with the incorrect option (`"It automatically stops and returns 0"`). The engine diagnoses the misconception: *Unbounded stack frame accumulation*.
5. **Teach Differently**: Click **"Teach Differently"**. The tutor presents the Russian Dolls analogy, traces `factorial(4)`, and poses a micro-check.
6. **Mastery Leap**: Answer the micro-check (`1`). Confetti triggers as Recursion mastery jumps **42% &rarr; 67% (+25%)**!
7. **Explainable Recommendation**: The Recommendation engine warns: *"Practice Recursion before Trees because Recursion is an essential prerequisite for tree traversal algorithms."*

---

## 11. API Documentation

Interactive Swagger documentation is available locally at:
👉 **`http://127.0.0.1:8000/docs`**

Key Endpoints:
- `GET /health`: Comprehensive system connectivity check (Python, SQLite, FAISS, Ollama).
- `POST /chat`: Grounded RAG tutoring with citation metadata.
- `POST /upload/pdf`: Ingest PDF textbooks with page-level citations.
- `POST /upload/slides`: Ingest PPTX slides with slide numbers.
- `POST /upload/video`: Ingest lecture video transcripts with timestamps.
- `POST /assessment/generate`: Dynamically generate assessment questions calibrated to student mastery.
- `POST /assessment/submit`: Submit answers, evaluate misconceptions, and update student mastery.
- `GET /progress`: Return overall learning health, weak topics, and strong topics.
- `GET /recommendations`: Explainable next topic recommendations.
- `POST /demo/reset`: Reset student state back to the 42% Recursion baseline for repeated judging.

---

## 12. Limitations & Future Work

- **Video Ingestion**: Audio extraction currently parses timestamped subtitle and transcript formats (`.vtt`, `.srt`, `.json`); live audio processing uses companion transcripts when local Whisper models are not initialized.
- **Multi-Course Scaling**: Currently seeded for Computer Science (Data Structures & Algorithms); can be extended to arbitrary academic domains.
- **Knowledge Tracing**: Future versions can incorporate Bayesian Knowledge Tracing (BKT) alongside the current explainable mastery formula.

---

## 13. AI-Assisted Development Disclosure

> In accordance with the official rules of the **Multimodal AI Hackathon 2026 (IIT Mandi / KamandPrompt)**, we transparently disclose:
>
> AI coding assistants were used during the development of LearnForge AI for rapid prototyping, architecture brainstorming, test authoring, UI component scaffolding, and documentation drafting. The team designed the core pedagogical loop, reviewed all system logic, validated the vector search and mastery algorithms, and is fully responsible for understanding, running, and explaining the final codebase.
