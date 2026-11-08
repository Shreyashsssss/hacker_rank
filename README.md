# SQL Edge-Case Eval

This project is a compact benchmark for a real limitation in modern AI systems: SQL reasoning under edge conditions.

## Why this gap matters

Frontier models can write straightforward SELECT statements, but they often miss the subtle logic that experienced analysts handle automatically:

- `NULL` semantics (`IS NULL` vs `= NULL`)
- date-window boundaries (`>= start AND < end`)
- duplicate groups and aggregation semantics
- zero-vs-null distinctions
- exclusion logic for cancelled or refunded records

These are not trick questions. They are everyday correctness problems in analytics and data engineering, and they are easy to verify with real test data.

## Eval structure

The benchmark contains five tasks. Each task includes:

1. a realistic SQL question,
2. a minimal SQLite schema,
3. a small dataset,
4. a correct answer in SQL,
5. a deterministic grader that compares the result set to the expected output.

Because the grader runs the candidate SQL against an in-memory SQLite database, the result is fully reproducible and has no ambiguity about what counts as a pass.

## How to run

```bash
python run_eval.py
```

You can also run the unit tests:

```bash
python -m unittest discover -s tests -q
```

## Scoring

Each task is scored as:

- `1.0` if the candidate SQL returns the exact expected rows
- `0.0` otherwise

The final score is the fraction of tasks passed. This avoids false positives from partial reasoning or fuzzy grading.

## Example failure modes the benchmark catches

- using `= NULL` instead of `IS NULL`
- using `<= end_date` when the correct logic is `< next_period_start`
- summing duplicate customers instead of grouping them correctly
- treating zero as missing data
- excluding valid orders because a refund row exists, even when the order was not cancelled

## Files

- `tasks.json` contains the benchmark tasks.
- `grader.py` executes candidate SQL and compares output to expected rows.
- `run_eval.py` runs a reference solution and a common-failure baseline.
- `tests/test_grader.py` verifies the grading logic.
