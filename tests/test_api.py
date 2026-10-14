import unittest
from fastapi.testclient import TestClient
from backend.main import app
from backend.demo_data import seed_demo_course

class TestApiEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_demo_course(force_reset=True)
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["components"]["database"], "connected")
        self.assertGreater(data["components"]["indexed_chunks"], 0)

    def test_progress_endpoint(self):
        response = self.client.get("/progress?student_id=demo-student-01")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("overall_health", data)
        self.assertIn("Recursion", data["weak_topics"])
        self.assertEqual(data["recommended_next"]["topic"], "Recursion")

    def test_course_materials_endpoint(self):
        response = self.client.get("/course/materials")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_ready"])
        self.assertGreater(len(data["materials"]), 0)

    def test_chat_endpoint_with_citations(self):
        payload = {
            "message": "Why does recursion require a base case?",
            "student_id": "demo-student-01",
            "topic": "Recursion",
            "mode": "Explain"
        }
        response = self.client.post("/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertEqual(data["topic"], "Recursion")
        self.assertGreater(len(data["citations"]), 0)
        # Check that citations have valid metadata
        first_cit = data["citations"][0]
        self.assertIn("source_name", first_cit)
        self.assertIn("timestamp_display", first_cit)

    def test_adaptive_assessment_flow(self):
        # 1. Generate Question
        gen_res = self.client.post("/assessment/generate", json={
            "topic": "Recursion",
            "student_id": "demo-student-01"
        })
        self.assertEqual(gen_res.status_code, 200)
        q = gen_res.json()
        self.assertIn("question_id", q)
        self.assertIn("prompt", q)

        # 2. Submit Wrong Answer to simulate student struggle
        sub_res = self.client.post("/assessment/submit", json={
            "student_id": "demo-student-01",
            "question_id": q["question_id"],
            "selected_answer": "Wrong option chosen"
        })
        self.assertEqual(sub_res.status_code, 200)
        eval_data = sub_res.json()
        self.assertFalse(eval_data["is_correct"])
        self.assertIsNotNone(eval_data["misconception_detected"])
        self.assertIsNotNone(eval_data["adaptive_teaching_recommendation"])

if __name__ == "__main__":
    unittest.main()
