import sys
import json
import codecs

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from backend.main import app

def test_full_system_flow():
    client = TestClient(app)
    print("=== 1. VERIFYING HEALTH ===")
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health_data = res.json()
    print(f"Health Status: {health_data['status']}")
    print(f"Indexed Chunks: {health_data['components']['indexed_chunks']}")
    print(f"Ollama Service: {health_data['components']['ollama_service']}")

    print("\n=== 2. VERIFYING INITIAL PROGRESS (HOME & MY PROGRESS) ===")
    res = client.get("/progress?student_id=demo-student-01")
    assert res.status_code == 200
    prog = res.json()
    print(f"Overall Health: {prog['overall_health']}%")
    print(f"Weak Topics: {prog['weak_topics']}")
    print(f"Strong Topics: {prog['strong_topics']}")
    print(f"Recommended Next: {prog['recommended_next']['target_concept']}")

    print("\n=== 3. VERIFYING AI TUTOR CHAT WITH GROUND-TRUTH CITATIONS ===")
    res = client.post("/chat", json={
        "message": "Why does recursion need a base case?",
        "mode": "Explain",
        "student_id": "demo-student-01"
    })
    assert res.status_code == 200
    chat_data = res.json()
    print(f"Tutor Response (preview): {chat_data['response'][:160]}...")
    print(f"Citations Retrieved: {len(chat_data['citations'])}")
    for cit in chat_data['citations']:
        print(f"  - [{cit['source_type']}] {cit['source_name']} ({cit.get('timestamp_display') or cit.get('page')}) -> Relevance: {cit.get('relevance_score')}")

    print("\n=== 4. VERIFYING PRACTICE QUIZ GENERATION & SUBMISSION ===")
    res = client.post("/assessment/generate", json={
        "topic": "Recursion",
        "student_id": "demo-student-01"
    })
    assert res.status_code == 200
    q = res.json()
    print(f"Generated Question: {q['prompt']}")
    print(f"Options ({len(q['options'])}): {q['options']}")

    # Submit an answer to verify misconception detection and feedback
    # Option B: "It automatically stops and returns 0" or an option that diagnoses misconception
    chosen_opt = q['options'][1]
    res = client.post("/assessment/submit", json={
        "question_id": q['question_id'],
        "selected_answer": chosen_opt,
        "student_id": "demo-student-01"
    })
    assert res.status_code == 200
    eval_res = res.json()
    print(f"Submitted: '{chosen_opt}'")
    print(f"Is Correct: {eval_res['is_correct']}")
    print(f"Misconception Diagnosed: {eval_res.get('misconception_detected')}")
    print(f"Explanation: {eval_res['explanation'][:120]}...")
    print(f"Mastery Transition: {int(eval_res['previous_mastery']*100)}% -> {int(eval_res['new_mastery']*100)}%")

    print("\n=== 5. VERIFYING TEACH ME DIFFERENTLY ADAPTIVE BREAKDOWN ===")
    res = client.post("/assessment/teach-differently", json={
        "topic": "Recursion",
        "attempt_count": 1,
        "student_id": "demo-student-01"
    })
    assert res.status_code == 200
    teach_data = res.json()
    print(f"Strategy: {teach_data['strategy_label']}")
    print(f"Title: {teach_data['title']}")
    if teach_data.get('mini_question'):
        print(f"Mini-Question: {teach_data['mini_question']['question']}")
        print(f"Correct Mini-Answer: {teach_data['mini_question']['correct_option']}")
    else:
        print(f"Content preview: {teach_data['content'][:120]}...")

    print("\n=== 6. VERIFYING DEMO RESET & PROGRESS UPDATE ===")
    res = client.post("/demo/reset", json={
        "student_id": "demo-student-01",
        "force_vector_reindex": False
    })
    assert res.status_code == 200
    reset_data = res.json()
    print(f"Reset Status: {reset_data.get('message', 'Reset OK')}")
    prog_after = client.get("/progress?student_id=demo-student-01").json()
    print(f"Post-Reset Health: {prog_after['overall_health']}%")

    print("\n=== 7. VERIFYING FRONTEND STATIC ASSET SERVING ===")
    res = client.get("/demo-ui")
    assert res.status_code == 200
    assert "LearnForge AI" in res.text or "<div id=\"root\">" in res.text
    print(f"Frontend dist /demo-ui status: 200 OK (Served {len(res.text)} bytes)")

    print("\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    test_full_system_flow()
