from typing import Optional

BASE_SYSTEM_PROMPT = """You are LearnForge AI, an expert adaptive educational AI tutor designed for Computer Science and Data Structures & Algorithms.

Your core mission:
1. Help the student achieve deep conceptual mastery.
2. Ground all knowledge in the student's provided course materials (textbook, slides, lecture transcripts).
3. Always maintain clear, rigorous pedagogical framing.
4. If course sources are provided in the context, refer to their key concepts and never invent false facts or hallucinatory citations.
5. If the course knowledge base does not contain the answer, state honestly: "The provided course materials do not cover this topic in detail, but conceptually...", and provide a helpful educational explanation.
"""

MODE_INSTRUCTIONS = {
    "Explain": (
        "Provide a clear, well-structured explanation. Highlight core principles, definitions, "
        "and practical relevance. Include bullet points and concise formatting."
    ),
    "Simplify": (
        "Explain this concept using simple, beginner-friendly language and intuitive everyday metaphors. "
        "Avoid overly dense jargon; focus on the 'aha!' moment."
    ),
    "Give Example": (
        "Provide a concrete, realistic code example and trace the execution step-by-step with small sample values."
    ),
    "Quiz Me": (
        "Formulate a diagnostic check question on this concept to test the student's understanding. "
        "Include multiple choice options or ask for output prediction."
    ),
    "Hint": (
        "Do NOT give away the complete answer. Provide a guiding hint or thought-provoking question "
        "to help the student deduce the solution themselves."
    ),
    "Challenge Me": (
        "Pose a challenging interview-level problem or subtle edge-case question related to this concept, "
        "testing time/space limits or boundary conditions."
    ),
    "Teach Differently": (
        "The student is struggling with the standard explanation. "
        "Pivot completely: use a vivid real-world analogy, a visual state breakdown, and a tiny intuitive checkpoint."
    )
}

def build_tutor_prompt(
    user_message: str,
    context_text: str,
    mode: str = "Explain",
    student_mastery: Optional[float] = None,
    topic: Optional[str] = None
) -> str:
    """Builds the comprehensive grounded prompt for the LLM."""
    mode_inst = MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS["Explain"])
    
    mastery_context = ""
    if student_mastery is not None:
        mastery_pct = int(student_mastery * 100)
        if mastery_pct < 50:
            mastery_context = (
                f"\n[Student Profile: Low Mastery ({mastery_pct}%) in {topic or 'this topic'}."
                " The student has struggled with previous questions. Keep explanations extra accessible and supportive.]"
            )
        elif mastery_pct > 80:
            mastery_context = (
                f"\n[Student Profile: High Mastery ({mastery_pct}%) in {topic or 'this topic'}."
                " The student is confident. You may explore advanced nuances and performance implications.]"
            )

    prompt = f"""[Instruction Mode: {mode}]
{mode_inst}
{mastery_context}

---
COURSE KNOWLEDGE CONTEXT (Retrieved from Student's Uploaded Materials):
{context_text if context_text else "No uploaded course documents match this query directly."}
---

STUDENT QUESTION:
{user_message}

Please respond to the student as LearnForge AI:"""

    return prompt
