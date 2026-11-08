# SQLTrap-Eval

SQLTrap-Eval is a reproducible benchmark designed to test whether frontier AI models can reason about SQL semantics rather than just generate syntactically plausible queries.

## Problem statement

Modern models can often produce valid SQL for straightforward CRUD and reporting tasks, but they are much less reliable when the query depends on subtle business logic: `NULL` handling, duplicate data, date boundaries, aggregation semantics, and join behavior.

The core research question is simple:

- Can the model produce a query that is correct under real-world edge conditions?
- Or does it just produce a SQL-looking answer that executes but fails semantically?

This benchmark focuses on those failure modes.

## What is included

This repository includes:

- a demo benchmark of SQL edge-case tasks,
- expert-style expected outputs,
- a deterministic SQLite grader,
- scripts to reproduce evaluation,
- a benchmark directory structure aligned to the research proposal.

## Repository layout

- [tasks.json](tasks.json): compact benchmark tasks used for local grading
- [grader.py](grader.py): SQLite result-based evaluator
- [run_eval.py](run_eval.py): sample benchmark runner
- [test_cases/demo_cases.json](test_cases/demo_cases.json): benchmark tasks and metadata
- [ground_truth/demo_expected.json](ground_truth/demo_expected.json): expected outputs
- [schemas/ecommerce_demo.sql](schemas/ecommerce_demo.sql): example schema
- [datasets/seed_demo_data.py](datasets/seed_demo_data.py): reproducible synthetic dataset generator
- [evaluation/run_sqltrap_eval.py](evaluation/run_sqltrap_eval.py): evaluation runner
- [reports/](reports/): generated benchmark reports

## Demo categories included

The current demo dataset covers:

1. NULL semantics
2. date and time boundaries
3. duplicate aggregation problems
4. zero-vs-null logic
5. join semantics and cancellation logic

## Run the demo

```bash
python run_eval.py
```

Or run the structured benchmark script:

```bash
python evaluation/run_sqltrap_eval.py
```

## Test the grader

```bash
python -m unittest discover -s tests -q
```

## Why this matters

This benchmark is intentionally built around problems that experienced analysts solve automatically:

- `= NULL` vs `IS NULL`
- month-end and midnight boundaries
- `COUNT(*)` vs `COUNT(column)`
- zero as a valid value, not a missing value
- cancelled vs refunded vs valid orders

These cases often pass syntax checks but fail in production reporting.

## Research direction

The project can be extended into a much larger benchmark with 30-50 cases across the eight categories listed in the master research brief: NULL semantics, join logic, grouping, window functions, date boundaries, boolean logic, and hidden perturbation sets.

This release is a working demo case proving the evaluation mechanism and grading approach.
