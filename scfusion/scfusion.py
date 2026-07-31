from pathlib import Path
import csv
import json

root = Path(__file__).resolve().parent
inputs = json.loads((root / "stage_inputs.json").read_text())
output_dir = root / "outputs"
output_dir.mkdir(exist_ok=True)

results = {}

for scenario, values in inputs.items():
    ground_truth = set(values["ground_truth"])
    foreman = set(values["foreman"])
    goleash = set(values["goleash"])

    unknown = (foreman | goleash) - ground_truth
    if unknown:
        raise ValueError(f"{scenario}: unknown stages: {sorted(unknown)}")

    fused = foreman | goleash
    missing = ground_truth - fused

    def coverage(stages):
        return len(stages & ground_truth) / len(ground_truth) * 100

    results[scenario] = {
        "ground_truth": sorted(ground_truth),
        "foreman": sorted(foreman),
        "goleash": sorted(goleash),
        "scfusion": sorted(fused),
        "missing": sorted(missing),
        "foreman_coverage": coverage(foreman),
        "goleash_coverage": coverage(goleash),
        "scfusion_coverage": coverage(fused)
    }

with (output_dir / "scfusion_results.json").open("w") as handle:
    json.dump(results, handle, indent=2)
    handle.write("\n")

with (output_dir / "scfusion_results.csv").open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow([
        "Scenario", "Stages", "Foreman", "GoLeash", "SCFusion",
        "Foreman Stages", "GoLeash Stages", "Fused Stages", "Missing"
    ])

    for scenario, result in results.items():
        writer.writerow([
            scenario,
            len(result["ground_truth"]),
            round(result["foreman_coverage"]),
            round(result["goleash_coverage"]),
            round(result["scfusion_coverage"]),
            "; ".join(result["foreman"]),
            "; ".join(result["goleash"]),
            "; ".join(result["scfusion"]),
            "; ".join(result["missing"])
        ])

print("| Scenario | Foreman | GoLeash | SCFusion |")
print("|---|---:|---:|---:|")

for scenario, result in results.items():
    print(
        f"| {scenario} | "
        f"{round(result['foreman_coverage'])}% | "
        f"{round(result['goleash_coverage'])}% | "
        f"{round(result['scfusion_coverage'])}% |"
    )
