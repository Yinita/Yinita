# Multi-Agent Evaluation Sample

This is a synthetic preview of the files delivered in a fixed-scope evaluation. It demonstrates the report shape only. It is not measured benchmark data and must not be used to claim one topology is better.

## Rebuild

Requires Python 3.10+ and the standard library only.

```powershell
python build_sample.py
```

The command validates `scenarios.jsonl`, rebuilds `results.jsonl` and `summary.csv`, and prints the aggregate table. The inputs deliberately use a mock model and synthetic outcomes.

## Files

- `scenarios.jsonl`: 12 small synthetic evaluation cases.
- `results.jsonl`: illustrative per-scenario outputs for three mock topologies.
- `summary.csv`: aggregate outcome, score, empty response, and estimated cost fields.
- `build_sample.py`: deterministic standard-library-only builder and validator.

## Real evaluation boundary

A real run needs a customer-authorized dataset, model endpoint or local runtime, scoring rubric, and an agreed hard spending cap. The customer retains control of credentials and API usage. No secret, private dataset, or user data is included here.
