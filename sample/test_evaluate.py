import json
import tempfile
import unittest
from pathlib import Path

from evaluate import summarize


class EvaluateTests(unittest.TestCase):
    def write_jsonl(self, directory, name, rows):
        path = Path(directory) / name
        path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
        return path

    def test_summarizes_complete_groups(self):
        with tempfile.TemporaryDirectory() as directory:
            scenarios = self.write_jsonl(directory, "scenarios.jsonl", [{"scenario_id": "a"}, {"scenario_id": "b"}])
            results = self.write_jsonl(directory, "results.jsonl", [
                {"scenario_id": "a", "dataset": "d", "model": "m", "topology": "single", "success": True, "response": "ok", "judge_score": 4, "estimated_cost_usd": 0.1},
                {"scenario_id": "b", "dataset": "d", "model": "m", "topology": "single", "success": False, "response": "", "judge_score": 2, "estimated_cost_usd": 0.2},
            ])
            summary = summarize(scenarios, results)[0]
            self.assertEqual(summary["task_success_rate"], 0.5)
            self.assertEqual(summary["mean_judge_score"], 3.0)
            self.assertEqual(summary["empty_response_rate"], 0.5)
            self.assertEqual(summary["estimated_cost_usd"], 0.3)

    def test_rejects_missing_scenario_result(self):
        with tempfile.TemporaryDirectory() as directory:
            scenarios = self.write_jsonl(directory, "scenarios.jsonl", [{"scenario_id": "a"}, {"scenario_id": "b"}])
            results = self.write_jsonl(directory, "results.jsonl", [
                {"scenario_id": "a", "dataset": "d", "model": "m", "topology": "single", "success": True, "response": "ok"},
            ])
            with self.assertRaisesRegex(ValueError, "exactly one result per scenario"):
                summarize(scenarios, results)


if __name__ == "__main__":
    unittest.main()
