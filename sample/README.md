# Multi-Agent Evaluation Toolkit

This free, local-first toolkit checks scenario-level agent results and produces a CSV summary. The included data is synthetic and demonstrates file formats only. It is not measured benchmark data and must not be used to claim one topology is better.

## Rebuild

Requires Python 3.10+ and the standard library only. Nothing is sent to a hosted service.

```powershell
python build_sample.py
python evaluate.py
python -m unittest -v
```

`build_sample.py` rebuilds the synthetic example. `evaluate.py` validates that each model/topology has exactly one result for every scenario, checks required fields and duplicate or unknown IDs, then writes `summary.csv`. `test_evaluate.py` covers summary calculations and incomplete-run rejection.

To evaluate your own files from another directory:

```powershell
python C:\path\to\sample\evaluate.py --scenarios scenarios.jsonl --results results.jsonl --output summary.csv
```

## Files

- `scenarios.jsonl`: 12 small synthetic evaluation cases.
- `results.jsonl`: illustrative per-scenario outputs for three mock topologies.
- `summary.csv`: aggregate outcome, score, empty response, and estimated cost fields.
- `build_sample.py`: deterministic standard-library-only builder and validator.
- `evaluate.py`: local JSONL validator and CSV report generator.
- `test_evaluate.py`: focused tests for calculations and incomplete data.

## Real evaluation boundary

A real run needs an authorized dataset, results from a model endpoint or local runtime, and a scoring rubric. The tool itself makes no model calls, so it requires no API key or API budget. This report does not act as an independent judge; scores must be supplied by the caller. Paid setup, rubric design, or failure analysis is available through the service page: https://yinita.github.io/Yinita/ai-evaluation.html
