# SQLTrap-Eval

SQLTrap-Eval is a reproducible benchmark designed to test whether frontier AI models can reason about SQL semantics rather than simply generate syntactically plausible queries.

## Problem statement

Modern models often succeed on basic SELECT and JOIN tasks but fail on edge cases that matter in real business analytics: `NULL` logic, duplicate rows, date boundaries, grouping semantics, window functions, and join behavior.

This benchmark targets those failures directly.

## What is now included

This repository now contains a fuller benchmark prototype covering multiple categories:

- NULL semantics
- duplicate records and aggregation
- date and time boundaries
- join semantics
- grouping and HAVING logic
- window functions and ranking
- boolean precedence and conditional expressions
- empty-result and missing-relationship edge cases

The suite is stored in [test_cases/sqltrap_cases.json](test_cases/sqltrap_cases.json) and evaluated by [evaluation/scorer.py](evaluation/scorer.py).

## Repository layout

- [run_eval.py](run_eval.py): benchmark runner for the expanded suite
- [grader.py](grader.py): original SQLite grader used by the demo tasks
- [tasks.json](tasks.json): earlier compact demo tasks
- [test_cases/sqltrap_cases.json](test_cases/sqltrap_cases.json): expanded benchmark suite
- [evaluation/scorer.py](evaluation/scorer.py): deterministic scoring logic
- [evaluation/run_sqltrap_eval.py](evaluation/run_sqltrap_eval.py): evaluation runner for reports
- [datasets/seed_demo_data.py](datasets/seed_demo_data.py): synthetic demo data generator
- [schemas/ecommerce_demo.sql](schemas/ecommerce_demo.sql): example schema
- [ground_truth/demo_expected.json](ground_truth/demo_expected.json): expected outputs for the original demo tasks
- [reports/](reports/): generated benchmark reports

## Run the expanded benchmark

```bash
python run_eval.py
```

This loads the category-rich suite and reports per-task and per-category results.

## Run the demo report script

```bash
python evaluation/run_sqltrap_eval.py
```

## Test the grader

```bash
python -m unittest discover -s tests -q
```

## Why this extension matters

The benchmark is intentionally designed around edge cases that experienced analysts catch automatically:

- `= NULL` vs `IS NULL`
- month-end and midnight boundaries
- `COUNT(*)` vs `COUNT(column)`
- zero as a valid value, not a missing value
- cancellations vs valid orders
- ranking ties and partition logic

These are real-world semantic issues, not trick SQL puzzles.

## Roadmap

The current repo is a strong benchmark prototype. It can be extended toward the broader research brief by adding:

- more hidden perturbation datasets,
- more category-specific cases,
- a leaderboard for multiple AI models,
- CSV/JSON export for reproducible comparison,
- a final report with category-wise failure analysis.
