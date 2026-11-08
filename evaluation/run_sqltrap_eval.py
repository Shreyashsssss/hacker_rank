import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "test_cases" / "demo_cases.json"
REPORT_PATH = ROOT / "reports" / "latest_demo_report.json"


def load_tasks(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)["tasks"]


def grade_sql(task, candidate_sql):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript(task["schema_sql"])
    for statement in task["inserts"]:
        cur.execute(statement)
    try:
        result = cur.execute(candidate_sql).fetchall()
    except Exception as exc:
        return {"passed": False, "score": 0.0, "error": str(exc), "actual": []}

    columns = [description[0] for description in cur.execute(candidate_sql).description] if result else []
    formatted = [dict(zip(columns, row)) for row in result]
    passed = formatted == task["expected_rows"]
    return {"passed": passed, "score": 1.0 if passed else 0.0, "actual": formatted}


def main():
    tasks = load_tasks(TASKS_PATH)
    report = {"benchmark": "SQLTrap-Eval Demo", "summary": {"total_tasks": len(tasks), "passed": 0}, "results": []}

    for task in tasks:
        score = grade_sql(task, task["reference_query"])
        item = {"id": task["id"], "category": task["category"], "passed": score["passed"], "score": score["score"], "actual": score["actual"]}
        report["results"].append(item)
        if score["passed"]:
            report["summary"]["passed"] += 1

    report["summary"]["accuracy"] = report["summary"]["passed"] / report["summary"]["total_tasks"]
    REPORT_PATH.parent.mkdir(exist_ok=True, parents=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
