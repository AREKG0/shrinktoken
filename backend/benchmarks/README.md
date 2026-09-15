# ShrinkToken Pro Benchmark Suite

## Overview
This directory contains the evaluation and benchmark suite for ShrinkToken Pro, measuring compression performance, safety preservation, false pass / false fail rates, and latency overhead across synthetic prompt datasets.

## Directory Structure
- `prompts/`: Category JSON datasets containing test prompts and expected constraints.
- `results/`: Output directory storing `latest_results.json`, `latest_results.csv`, and `summary.json`.
- `runner.py`: Benchmark orchestrator executing compression, validation, and metrics calculation.
- `evaluator.py`: `SemanticEvaluator` interface for property-based fidelity checking.
- `metrics.py`: Metric calculator aggregating token reductions, latency, and category statistics.

## How to Run Benchmarks

Run full benchmark:
```powershell
$env:PYTHONPATH="D:\shrinktoken-pro"; D:\shrinktoken-pro\venv\Scripts\python.exe D:\shrinktoken-pro\backend\benchmarks\runner.py
```

Run test suite:
```powershell
$env:PYTHONPATH="D:\shrinktoken-pro"; D:\shrinktoken-pro\venv\Scripts\pytest.exe D:\shrinktoken-pro\backend\tests\ -v
```
