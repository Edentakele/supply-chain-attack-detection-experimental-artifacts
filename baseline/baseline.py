from parser import collect_artifact_inventory


def evaluate_scenario(base_directory, configuration, include_archived_creations=True):
    inventory = collect_artifact_inventory(
        base_directory, configuration['directories'], include_archived_creations
    )
    ground_truth = set(configuration['ground_truth'])
    detected = set()
    matched_rules = []
    for artifact, stage in configuration['rules'].items():
        sources = inventory.get(artifact.lower(), [])
        if sources:
            detected.add(stage)
            matched_rules.append({'artifact': artifact.lower(), 'stage': stage,
                                  'sources': sources})
    unknown = detected - ground_truth
    if unknown:
        raise ValueError(f'Detected stages outside ground truth: {sorted(unknown)}')
    matched = detected & ground_truth
    exact_coverage = len(matched) / len(ground_truth) * 100
    return {
        'ground_truth': sorted(ground_truth), 'detected': sorted(matched),
        'missing': sorted(ground_truth - matched), 'matched_rules': matched_rules,
        'exact_coverage': exact_coverage, 'reported_coverage': round(exact_coverage),
        'inventory_mode': 'retained-files-plus-archived-creations' if include_archived_creations else 'retained-files-only'
    }
