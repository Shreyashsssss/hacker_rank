import json
import sqlite3
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "test_cases" / "sqltrap_cases.json"


def load_tasks(path: Path = CASES_PATH):
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload["tasks"]


def normalize_rows(result_rows, columns):
    if not result_rows:
        return []
    return [dict(zip(columns, row)) for row in result_rows]


def grade_task(task, candidate_sql):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript(task["schema_sql"])
    for statement in task["inserts"]:
        for sql in [part.strip() for part in statement.split(";") if part.strip()]:
            cur.execute(sql)

    try:
        cur_result = cur.execute(candidate_sql)
        rows = cur_result.fetchall()
        columns = [d[0] for d in cur_result.description] if cur_result.description else []
        actual = normalize_rows(rows, columns)
    except Exception as exc:
        return {"passed": False, "score": 0.0, "actual": [], "error": str(exc)}

    expected = task.get("expected_rows", [])
    passed = actual == expected
    return {"passed": passed, "score": 1.0 if passed else 0.0, "actual": actual, "expected": expected}


def evaluate_suite(path: Path = CASES_PATH):
    tasks = load_tasks(path)
    category_scores = defaultdict(list)
    results = []
    total = 0
    passed = 0

    for task in tasks:
        total += 1
        score = grade_task(task, task["reference_query"])
        category_scores[task["category"]].append(score["score"])
        results.append({
            "id": task["id"],
            "category": task["category"],
            "difficulty": task.get("difficulty", "medium"),
            "passed": score["passed"],
            "score": score["score"],
        })
        if score["passed"]:
            passed += 1

    summary = {
        "total_tasks": total,
        "passed": passed,
        "accuracy": passed / total if total else 0.0,
        "categories": {
            category: {
                "tasks": len(values),
                "passed": sum(values),
                "accuracy": sum(values) / len(values) if values else 0.0,
            }
            for category, values in category_scores.items()
        },
    }
    return {"summary": summary, "results": results}


def main():
    report = evaluate_suite()
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
