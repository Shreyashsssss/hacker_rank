import json
from typing import Dict, List

from grader import grade_answer


def load_tasks(path: str = "tasks.json") -> List[Dict]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload["tasks"]


def default_candidate_map(tasks: List[Dict]) -> Dict[str, Dict[str, str]]:
    reference = {}
    common_failure = {}
    for task in tasks:
        reference[task["id"]] = task["reference_query"]
        common_failure[task["id"]] = task.get("wrong_query") or task["reference_query"]
    return {"reference": reference, "common_failure": common_failure}


def main() -> None:
    tasks = load_tasks()
    candidates = default_candidate_map(tasks)

    for candidate_name, answers in candidates.items():
        total = 0
        passed = 0
        print(f"\n== {candidate_name} ==")
        for task in tasks:
            score = grade_answer(task, answers.get(task["id"], ""))
            total += 1
            if score["passed"]:
                passed += 1
            print(f"- {task['id']}: {'PASS' if score['passed'] else 'FAIL'} ({score['score']:.0%})")
        print(f"Summary: {passed}/{total} tasks passed")


if __name__ == "__main__":
    main()
