import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.scorer import evaluate_suite

REPORT_PATH = ROOT / "reports" / "latest_demo_report.json"


def main():
    report = evaluate_suite(ROOT / "test_cases" / "sqltrap_cases.json")
    REPORT_PATH.parent.mkdir(exist_ok=True, parents=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
