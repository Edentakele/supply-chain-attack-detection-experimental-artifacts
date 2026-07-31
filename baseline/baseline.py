from parser import collect_filenames


def evaluate_scenario(base_directory, configuration):
    evidence = collect_filenames(
        base_directory,
        configuration["directories"],
    )

    ground_truth = set(configuration["ground_truth"])
    detected = set()
    matched_rules = []

    for artifact, stage in configuration["rules"].items():
        if artifact.lower() in evidence:
            detected.add(stage)
            matched_rules.append({
                "artifact": artifact.lower(),
                "stage": stage,
            })

    unknown = detected - ground_truth
    if unknown:
        raise ValueError(
            f"Detected stages outside ground truth: {sorted(unknown)}"
        )

    matched = detected & ground_truth
    missing = ground_truth - matched
    exact_coverage = len(matched) / len(ground_truth) * 100
    reported_coverage = round(exact_coverage)

    return {
        "ground_truth": sorted(ground_truth),
        "detected": sorted(matched),
        "missing": sorted(missing),
        "matched_rules": matched_rules,
        "exact_coverage": exact_coverage,
        "reported_coverage": reported_coverage,
    }
