import unittest
from backend.student.mastery import calculate_mastery
from backend.assessment.evaluator import evaluate_student_answer
from backend.assessment.question_generator import get_question_by_id
from backend.student.recommendations import generate_explainable_recommendation
from backend.demo_data import seed_demo_course

class TestMasteryAndAdaptiveEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_demo_course(force_reset=True)

    def test_mastery_formula(self):
        # Formula: 0.5 * accuracy + 0.3 * diff_factor + 0.2 * consistency
        # For accuracy=0.8, diff="MEDIUM" (0.85), consistency=0.8:
        # 0.5 * 0.8 + 0.3 * 0.85 + 0.2 * 0.8 = 0.40 + 0.255 + 0.16 = 0.815 -> 0.82
        m = calculate_mastery(recent_accuracy=0.8, difficulty_reached="MEDIUM", consistency_score=0.8)
        self.assertAlmostEqual(m, 0.82, places=2)

        # Clamping check
        m_clamped = calculate_mastery(recent_accuracy=1.5, difficulty_reached="HARD", consistency_score=1.5)
        self.assertEqual(m_clamped, 1.0)

    def test_evaluator_correct_and_incorrect(self):
        # Question rec-m-01
        q = get_question_by_id("rec-m-01")
        self.assertIsNotNone(q)

        # Incorrect answer
        is_corr, exp, expl, misc = evaluate_student_answer("rec-m-01", "It automatically stops and returns 0 after 1000 cycles")
        self.assertFalse(is_corr)
        self.assertIn("StackOverflowError", exp)
        self.assertIsNotNone(misc)

        # Correct answer
        is_corr, exp, expl, misc = evaluate_student_answer("rec-m-01", "It runs until memory limit is exceeded, causing a StackOverflowError")
        self.assertTrue(is_corr)

    def test_explainable_recommendation(self):
        # Demo user initial state has Recursion at 42% (< 60%) and Trees at 51%
        rec = generate_explainable_recommendation("demo-student-01")
        self.assertIn("Recursion", rec["topic"])
        self.assertIn("42%", rec["reason"])
        self.assertIn("prerequisite", rec["reason"].lower())

if __name__ == "__main__":
    unittest.main()
