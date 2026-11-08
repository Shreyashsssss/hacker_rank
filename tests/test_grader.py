import sqlite3
import unittest

from grader import grade_answer


class GraderTests(unittest.TestCase):
    def test_rejects_wrong_null_logic(self):
        task = {
            "id": "null_logic",
            "question": "List customer ids whose cancelled_at is NULL and paid_at is not NULL.",
            "expected_rows": [
                {"customer_id": 2},
                {"customer_id": 3},
            ],
            "schema": "CREATE TABLE orders (customer_id INTEGER, paid_at TEXT, cancelled_at TEXT);",
            "rows": [
                (1, "2025-01-01", "2025-01-02"),
                (2, "2025-01-03", None),
                (3, "2025-01-05", None),
                (4, None, None),
            ],
        }

        candidate = "SELECT customer_id FROM orders WHERE cancelled_at IS NULL AND paid_at IS NOT NULL ORDER BY customer_id;"
        score = grade_answer(task, candidate)
        self.assertEqual(score["passed"], True)
        self.assertEqual(score["score"], 1.0)

        wrong = "SELECT customer_id FROM orders WHERE cancelled_at = NULL AND paid_at IS NOT NULL ORDER BY customer_id;"
        bad_score = grade_answer(task, wrong)
        self.assertEqual(bad_score["passed"], False)
        self.assertLess(bad_score["score"], 1.0)

    def test_catches_inclusive_date_boundary_error(self):
        task = {
            "id": "date_boundary",
            "question": "Return orders with order_date in the month of June 2025, inclusive of the 30th but not July 1st.",
            "expected_rows": [
                {"order_id": 1},
                {"order_id": 2},
            ],
            "schema": "CREATE TABLE orders (order_id INTEGER, order_date TEXT);",
            "rows": [
                (1, "2025-06-15T10:00:00"),
                (2, "2025-06-30T12:00:00"),
                (3, "2025-07-01T00:00:00"),
                (4, "2025-05-31T23:59:59"),
            ],
        }

        candidate = "SELECT order_id FROM orders WHERE order_date >= '2025-06-01' AND order_date < '2025-07-01' ORDER BY order_id;"
        score = grade_answer(task, candidate)
        self.assertTrue(score["passed"])

        wrong = "SELECT order_id FROM orders WHERE order_date >= '2025-06-01' AND order_date <= '2025-06-30' ORDER BY order_id;"
        bad_score = grade_answer(task, wrong)
        self.assertFalse(bad_score["passed"])


if __name__ == "__main__":
    unittest.main()
