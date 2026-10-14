# LearnForge AI — Beginner-Friendly Student Learning Guide

Welcome to the comprehensive learning guide for **LearnForge AI**. This guide explains all 15 core concepts of this project in simple, clear terms so you can confidently understand and explain your architecture to hackathon judges.

For each concept, we break down:
- **WHY it exists** (The real problem it solves)
- **WHAT it does** (Its role in the system)
- **HOW it works** (The code and mechanics behind it)

---

## 1. What FastAPI Does
- **WHY**: A web application needs a reliable way for the browser (frontend) to send user questions and receive answers from Python AI models and databases.
- **WHAT**: FastAPI is a modern, high-performance Python web framework used to build REST APIs.
- **HOW**: FastAPI uses Python type hints (`pydantic`) to validate incoming JSON requests and automatically produce interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## 2. What Embeddings Are
- **WHY**: Computers cannot calculate the conceptual meaning of words using simple text matching. For example, "divide and conquer" and "halving the search interval" mean the same thing, but share no words.
- **WHAT**: An embedding converts a sentence into a list of numbers (a vector) where sentences with similar meanings end up close together in mathematical space.
- **HOW**: We use `all-MiniLM-L6-v2` via `sentence-transformers`. It turns each text chunk into a 384-number vector. We normalize the vector so that computing the dot product calculates cosine similarity directly.

---

## 3. What FAISS Does
- **WHY**: If you have thousands of textbook paragraphs, comparing your question to every single paragraph sequentially is too slow.
- **WHAT**: FAISS (Facebook AI Similarity Search) is a specialized C++/Python library for lightning-fast vector search.
- **HOW**: FAISS stores vectors in an index (`IndexFlatIP`). When a query arrives, FAISS compares the query vector against all chunk vectors simultaneously and returns the top 3 closest chunks in less than 2 milliseconds.

---

## 4. What RAG (Retrieval-Augmented Generation) Is
- **WHY**: Standard LLMs hallucinate facts and do not know what is inside a student's specific professor slides or textbook.
- **WHAT**: RAG retrieves relevant facts from verified documents first, and inserts them into the prompt before the LLM generates an answer.
- **HOW**: 
  1. Student asks: *"What is binary search?"*
  2. Embed question $\to$ Search FAISS $\to$ Find Textbook Page 42.
  3. Prompt LLM: *"Using only this textbook excerpt from Page 42, explain binary search."*
  4. LLM answers using the excerpt and cites the textbook.

---

## 5. How PDF Ingestion Works
- **WHY**: Textbooks are published in PDF format with complex binary stream structures.
- **WHAT**: `backend/ingestion/pdf_loader.py` reads PDFs and extracts clean text page-by-page.
- **HOW**: We use `pypdf.PdfReader`. It extracts text for each page, removes extra whitespace, and attaches the 1-indexed page number (`page: 42`) so citations match the physical book.

---

## 6. How Video/Lecture Transcription Works
- **WHY**: Students watch hours of lecture videos and need to jump to the exact minute an algorithm was explained.
- **WHAT**: `backend/ingestion/transcript.py` parses subtitle and transcript formats (`.vtt`, `.srt`, `.json`) into timestamped segments.
- **HOW**: A regular expression extracts time intervals like `00:12:34.000 --> 00:13:09.000`. The parser converts `12:34` into `754.0` seconds and formats a display string `"12:34"` for citations.

---

## 7. How Metadata Citations Work
- **WHY**: If a tutor claims an answer is from the slides, the student must be able to verify it. Citations must never be fabricated.
- **WHAT**: `backend/knowledge/metadata.py` packages the source type, name, page, slide, and timestamp with every chunk.
- **HOW**: Each chunk dictionary carries `{source_type: 'slides', slide: 17, source_name: 'Searching Slides'}`. The frontend renders this as a clickable chip `[Slides · Slide 17]`. Clicking it opens the modal with the exact extracted excerpt.

---

## 8. How the LLM Receives Context
- **WHY**: The LLM needs strict boundaries to avoid making up answers.
- **WHAT**: `backend/tutor/prompts.py` builds the prompt context.
- **HOW**: The system injects retrieved excerpts into a structured template:
  ```
  COURSE KNOWLEDGE CONTEXT:
  [Source #1 | Textbook · p.58 | Topic: Recursion]
  A recursive algorithm must have a base case to prevent stack overflow...
  
  STUDENT QUESTION:
  Why does recursion need a base case?
  ```
  The LLM reads this context and synthesizes a grounded answer.

---

## 9. How Quiz Generation Works
- **WHY**: Students need practice questions matched to their actual understanding, not random trivia.
- **WHAT**: `backend/assessment/adaptive_engine.py` generates questions tailored to student mastery.
- **HOW**: If the student's mastery in Recursion is low (42%), the engine serves an `EASY` or `MEDIUM` diagnostic question focusing on foundational mechanics.

---

## 10. How Mastery is Calculated
- **WHY**: We need an explainable number ($0.0 \sim 1.0$) representing student learning progress without black-box guessing.
- **WHAT**: `backend/student/mastery.py` implements the formula:
  $$\text{mastery} = 0.50 \times \text{recent\_accuracy} + 0.30 \times \text{difficulty\_factor} + 0.20 \times \text{consistency}$$
- **HOW**: 
  - Accuracy: $\frac{\text{correct}}{\text{attempts}}$.
  - Difficulty: 0.6 for Easy, 0.85 for Medium, 1.0 for Hard.
  - Consistency: 0.8 for streaks.
  The result is clamped between 0.0 and 1.0 and displayed as a percentage.

---

## 11. How Weak Topics are Detected
- **WHY**: Students often do not realize which prerequisite concept is holding them back.
- **WHAT**: `backend/student/profile.py` categorizes topics:
  - **Weak (< 60%)**: Needs immediate attention (e.g. Recursion at 42%).
  - **Competent (60% - 74%)**: Good understanding (e.g. Sorting at 72%).
  - **Strong ($\ge$ 75%)**: Solid grasp (e.g. Binary Search at 85%).
- **HOW**: A SQL query orders topics by mastery ascending, immediately flagging topics with score $< 0.60$.

---

## 12. How Adaptive Teaching Works (Teach Differently)
- **WHY**: When a student gets a question wrong, repeating the exact same textbook definition will not help them learn.
- **WHAT**: `backend/tutor/strategies.py` switches explanation strategies:
  1. Technical Explanation $\to$
  2. Intuitive Analogy (Russian Nesting Dolls) $\to$
  3. Step-by-Step Worked Example (`factorial(4)` trace) $\to$
  4. Micro-Check Practice Question.
- **HOW**: When the student misses a question or clicks "Teach Differently", the tutor delivers Strategy 2 or 3 instead of repeating Strategy 1.

---

## 13. How Recommendations Work
- **WHY**: Students ask: *"What should I learn next?"*
- **WHAT**: `backend/student/recommendations.py` provides explainable recommendations based on a prerequisite tree.
- **HOW**: Trees require Recursion. If Trees is attempted while Recursion is at 42%, the engine recommends:
  *"Practice Recursion before Trees because Recursion is an essential prerequisite for tree traversal algorithms."*

---

## 14. How Frontend Talks to Backend
- **WHY**: React runs in the browser, while Python runs as a local server.
- **WHAT**: `frontend/src/services/api.js` makes HTTP requests using the browser's `fetch` API.
- **HOW**: When a student clicks "Submit Answer", React calls `POST http://127.0.0.1:8000/assessment/submit`. FastAPI parses the JSON, calculates the new mastery score in SQLite, and returns the response in milliseconds.

---

## 15. How the Database Stores Progress
- **WHY**: If the browser refreshes, the student's progress and quiz history must not disappear.
- **WHAT**: SQLite (`data/learnforge.db`) stores courses, chunks, student profiles, topic mastery, and attempt history.
- **HOW**: SQLite is an embedded SQL database stored in a single file on disk, requiring zero complex server setup while providing complete ACID transactions.
