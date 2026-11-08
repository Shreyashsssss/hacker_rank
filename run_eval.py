import json
from typing import Dict, List

from evaluation.scorer import evaluate_suite


def load_tasks(path: str = "test_cases/sqltrap_cases.json") -> List[Dict]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload["tasks"]


def main() -> None:
    tasks = load_tasks()
    report = evaluate_suite()

    print("\n== SQLTrap-Eval Expanded Benchmark ==")
    print(f"Total tasks: {report['summary']['total_tasks']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Accuracy: {report['summary']['accuracy']:.2%}")

    for result in report["results"]:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"- {result['id']} [{result['category']}]: {status}")

    print("\nCategory summary:")
    for category, summary in report["summary"]["categories"].items():
        print(f"- {category}: {summary['passed']}/{summary['tasks']} ({summary['accuracy']:.2%})")


if __name__ == "__main__":
    main()
