# LearnForge AI — Hackathon Winning Demo Script (3 Minutes)

Use this exact script for presenting to judges at the **Multimodal AI Hackathon 2026 (IIT Mandi / KamandPrompt)**.

---

## Timecode Walkthrough

### 0:00 — The Problem (30 seconds)
> *"Hello judges. Students today have lecture video recordings, slide decks, and textbooks scattered everywhere. Typical AI study tools are just standard ChatGPT wrappers with PDF uploads. They answer one question, but they have no idea what the student actually understands."*
>
> *"We built **LearnForge AI: Your Adaptive AI Learning Companion**. It goes beyond document Q&A to track student mastery, diagnose misconceptions, and change how it teaches."*

---

### 0:30 — Unified Multimodal Knowledge Base (30 seconds)
> *(Navigate to **"My Course & Sources"** or point to Dashboard)*
>
> *"Here in our Data Structures & Algorithms course, we ingested three different multimodal sources:*
> 1. *A PDF textbook: 'Data Structures & Algorithm Analysis'*
> 2. *A PowerPoint slide deck: 'Searching & Sorting Masterclass'*
> 3. *A timestamped lecture video transcript: 'DSA Lecture 3'*
>
> *LearnForge AI extracted and indexed all three into a local FAISS vector knowledge base with page numbers, slide numbers, and video timestamps preserved."*

---

### 1:00 — Grounded AI Tutor & Exact Citations (30 seconds)
> *(Navigate to **"Ask Tutor"**)*
>
> *"Let's ask the tutor: **'Why does recursion need a base case?'**"*
>
> *(Point to the response and citation chips)*
>
> *"Notice the answer is strictly grounded in our course materials. Look at the citation chips:*
> - `[📘 Textbook · p.58]`
> - `[🎥 Lecture · 12:34]`
>
> *When we click `Textbook · p.58`, it opens the verified excerpt directly from the textbook. And if we expand our **RAG Inspector**, you can see the raw cosine similarity score from FAISS. There are zero hallucinations."*

---

### 1:30 — Adaptive Assessment & Concept Gap Detection (45 seconds)
> *(Navigate to **"Practice & Quiz"**)*
>
> *"Now the student clicks **'Continue Diagnostic Check'** on Recursion. Notice our student, Alex, currently has a low mastery of **42%**.*
>
> *The system generates a question calibrated to this level:*
> *'What happens if a recursive function is invoked without a valid base case?'*
>
> *Suppose the student chooses the common misconception: 'It automatically stops and returns 0 after 1000 cycles.'*
>
> *(Click submit)*
>
> *The system immediately flags:*
> - *Incorrect!*
> - *Diagnosed Misconception: The student believes runtimes safely cap recursion.*
> - *Concept gap detected: recursion base cases and stack limits."*

---

### 2:15 — The "Wow" Feature: Teach Differently (45 seconds)
> *(Click the glowing **"Teach Me Differently"** button)*
>
> *"Most educational AI chatbots would just repeat the textbook definition again. LearnForge AI switches strategy!*
>
> *It pivots to **Strategy 2: The Russian Nesting Dolls Analogy** and traces `factorial(4)` step by step on the call stack.*
>
> *Then it serves a targeted micro-check: 'When n==1 evaluates, what value is returned to unstack?'*
>
> *(Select '1' and submit)*
>
> *Correct! Look at what just happened:*
> *Recursion mastery jumps from **42% to 67% (+25%)**.*
> *Our student model updated dynamically in real-time."*

---

### 2:50 — Explainable Next Topic Recommendation & Closing (30 seconds)
> *(Navigate back to **"Dashboard"**)*
>
> *"Look at our Dashboard now. The Learning Health improved, and our Recommendation Engine warns:*
> *'You should practice Recursion before Trees because your recursion mastery is currently 67% (Recursion is an essential prerequisite for tree traversals).'*
>
> *The system explains WHY, based on the course prerequisite graph.*
>
> *To conclude:*
> **'Most educational AI systems answer what students ask. LearnForge AI remembers what they struggle with and changes what it teaches next.'**
>
> *Thank you! We welcome your questions."*
