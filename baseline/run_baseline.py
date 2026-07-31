from pathlib import Path
import csv
import json

from baseline import evaluate_scenario
from scenarios import SCENARIOS


root = Path(__file__).resolve().parent
outputs = root / "outputs"
outputs.mkdir(exist_ok=True)

results = {}

for scenario, configuration in SCENARIOS.items():
    results[scenario] = evaluate_scenario(root, configuration)

with (outputs / "baseline_results.json").open("w") as handle:
    json.dump(results, handle, indent=2)
    handle.write("\n")

with (outputs / "baseline_results.csv").open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow([
        "Scenario",
        "Stages",
        "Detected Stage",
        "Matched Artifact",
        "Coverage",
    ])

    for scenario, result in results.items():
        writer.writerow([
            scenario,
            len(result["ground_truth"]),
            "; ".join(result["detected"]),
            "; ".join(
                rule["artifact"]
                for rule in result["matched_rules"]
            ),
            result["reported_coverage"],
        ])

average = (
    sum(result["reported_coverage"] for result in results.values())
    / len(results)
)

with (outputs / "baseline_summary.txt").open("w") as handle:
    for scenario, result in results.items():
        handle.write(
            f"{scenario}: "
            f"{result['reported_coverage']}% "
            f"({', '.join(result['detected'])})\n"
        )

    handle.write(f"\nAverage coverage: {average:.1f}%\n")

print("| Scenario | Stages | Baseline | Detected Stage |")
print("|---|---:|---:|---|")

for scenario, result in results.items():
    print(
        f"| {scenario} | "
        f"{len(result['ground_truth'])} | "
        f"{result['reported_coverage']}% | "
        f"{', '.join(result['detected'])} |"
    )

print(f"\nAverage baseline coverage: {average:.1f}%")
