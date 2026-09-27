import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCENARIOS = ROOT / "scenarios.jsonl"
RESULTS = ROOT / "results.jsonl"
SUMMARY = ROOT / "summary.csv"
TOPOLOGIES = {
    "single": {"successes": 7, "score": 3.2, "cost": 0.02},
    "central": {"successes": 8, "score": 3.5, "cost": 0.07},
    "debate": {"successes": 9, "score": 3.8, "cost": 0.13},
}


def read_scenarios():
    rows = [json.loads(line) for line in SCENARIOS.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 12 or len({row["scenario_id"] for row in rows}) != len(rows):
        raise ValueError("Expected 12 uniquely identified synthetic scenarios")
    return rows


def main():
    scenarios = read_scenarios()
    results = []
    summaries = []
    for topology, spec in TOPOLOGIES.items():
        success_count = spec["successes"]
        for index, scenario in enumerate(scenarios):
            success = index < success_count
            results.append({
                "scenario_id": scenario["scenario_id"],
                "dataset": "demo-synthetic-v1",
                "model": "mock-model",
                "topology": topology,
                "success": success,
                "judge_score": round(spec["score"] if success else max(1, spec["score"] - 1), 1),
                "response": f"Synthetic {topology} response for {scenario['scenario_id']}" if success else "",
                "estimated_cost_usd": round(spec["cost"] / len(scenarios), 8),
            })
        summaries.append({
            "dataset": "demo-synthetic-v1",
            "model": "mock-model",
            "scenario_count": len(scenarios),
            "topology": topology,
            "task_success_rate": round(success_count / len(scenarios), 4),
            "mean_judge_score": round(sum(spec["score"] if index < success_count else max(1, spec["score"] - 1) for index in range(len(scenarios))) / len(scenarios), 4),
            "empty_response_rate": 0.0,
            "estimated_cost_usd": spec["cost"],
            "notice": "Synthetic demonstration only; not a measured result.",
        })

    RESULTS.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in results), encoding="utf-8")
    with SUMMARY.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=summaries[0].keys())
        writer.writeheader()
        writer.writerows(summaries)
    print(f"Wrote {len(results)} synthetic rows across {len(TOPOLOGIES)} topologies")
    for row in summaries:
        print(f"{row['topology']}: success={row['task_success_rate']:.0%}, cost=${row['estimated_cost_usd']:.2f}")


if __name__ == "__main__":
    main()
