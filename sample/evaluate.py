import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


REQUIRED = {"scenario_id", "dataset", "model", "topology", "success", "response"}


def load_jsonl(path):
    rows = []
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_number}: each JSONL line must be an object")
        rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no records found")
    return rows


def summarize(scenarios_path, results_path):
    scenarios = load_jsonl(scenarios_path)
    results = load_jsonl(results_path)
    scenario_ids = [row.get("scenario_id") for row in scenarios]
    if any(not isinstance(value, str) or not value for value in scenario_ids):
        raise ValueError("Every scenario needs a non-empty scenario_id")
    if len(set(scenario_ids)) != len(scenario_ids):
        raise ValueError("Scenario IDs must be unique")
    known_ids = set(scenario_ids)
    seen = set()
    groups = defaultdict(list)
    for index, row in enumerate(results, 1):
        missing = REQUIRED - row.keys()
        if missing:
            raise ValueError(f"Result {index} missing fields: {', '.join(sorted(missing))}")
        if not isinstance(row["success"], bool):
            raise ValueError(f"Result {index}: success must be true or false")
        if not isinstance(row["response"], str):
            raise ValueError(f"Result {index}: response must be a string")
        if row["scenario_id"] not in known_ids:
            raise ValueError(f"Result {index}: unknown scenario_id {row['scenario_id']!r}")
        key = (row["model"], row["topology"], row["scenario_id"])
        if key in seen:
            raise ValueError(f"Duplicate result for model/topology/scenario: {key}")
        seen.add(key)
        groups[(row["dataset"], row["model"], row["topology"])].append(row)

    expected = len(scenarios)
    summaries = []
    for (dataset, model, topology), rows in sorted(groups.items()):
        ids = {row["scenario_id"] for row in rows}
        if len(rows) != expected or ids != known_ids:
            raise ValueError(f"{model}/{topology}: expected exactly one result per scenario ({expected})")
        empty = sum(not row["response"].strip() for row in rows)
        scores = [row["judge_score"] for row in rows if isinstance(row.get("judge_score"), (int, float))]
        costs = [row["estimated_cost_usd"] for row in rows if isinstance(row.get("estimated_cost_usd"), (int, float))]
        summaries.append({
            "dataset": dataset,
            "model": model,
            "topology": topology,
            "scenario_count": len(rows),
            "task_success_rate": round(sum(row["success"] for row in rows) / len(rows), 4),
            "mean_judge_score": round(sum(scores) / len(scores), 4) if scores else "",
            "empty_response_rate": round(empty / len(rows), 4),
            "estimated_cost_usd": round(sum(costs), 6) if costs else "",
        })
    return summaries


def main():
    parser = argparse.ArgumentParser(description="Validate JSONL agent evaluation results and export a CSV summary.")
    parser.add_argument("--scenarios", default="scenarios.jsonl")
    parser.add_argument("--results", default="results.jsonl")
    parser.add_argument("--output", default="summary.csv")
    args = parser.parse_args()
    rows = summarize(args.scenarios, args.results)
    output = Path(args.output)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Validated {sum(row['scenario_count'] for row in rows)} results in {len(rows)} model/topology groups")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
