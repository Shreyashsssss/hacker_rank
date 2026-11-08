import sqlite3
from typing import Any, Dict, List


def _coerce_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (int, float, str, bool)):
        return value
    return str(value)


def _normalize_result(rows: List[tuple], columns: List[str]) -> List[Dict[str, Any]]:
    if not rows:
        return []
    normalized = []
    for row in rows:
        normalized.append({column: _coerce_value(value) for column, value in zip(columns, row)})
    return normalized


def _create_database(task: Dict[str, Any]) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    schema_sql = task.get("schema_sql") or task.get("schema")
    if schema_sql:
        if isinstance(schema_sql, list):
            for statement in schema_sql:
                cursor.execute(statement)
        else:
            cursor.executescript(schema_sql)

    inserts = task.get("inserts") or []
    if inserts:
        for statement in inserts:
            cursor.execute(statement)
    elif task.get("rows"):
        table_name = task.get("table_name") or "orders"
        for row in task["rows"]:
            placeholders = ", ".join("?" for _ in row)
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

    return connection


def grade_answer(task: Dict[str, Any], candidate_sql: str) -> Dict[str, Any]:
    """Execute a candidate SQL query against the task's SQLite schema and compare the output to the expected rows."""
    if not candidate_sql or not candidate_sql.strip():
        return {"passed": False, "score": 0.0, "actual": [], "expected": task.get("expected_rows", [])}

    connection = _create_database(task)
    cursor = connection.cursor()

    try:
        result = cursor.execute(candidate_sql)
        actual_rows = result.fetchall()
        columns = [column[0] for column in result.description] if result.description else []
        actual = _normalize_result(actual_rows, columns)
    except Exception as exc:  # pragma: no cover - error path is exercised by tests via bad SQL.
        return {
            "passed": False,
            "score": 0.0,
            "actual": [],
            "expected": task.get("expected_rows", []),
            "error": str(exc),
        }

    expected = task.get("expected_rows", [])
    if actual == expected:
        return {"passed": True, "score": 1.0, "actual": actual, "expected": expected}

    return {"passed": False, "score": 0.0, "actual": actual, "expected": expected}
