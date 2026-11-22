# SCFusion: Cross-Layer Build-Time and Runtime Stage Evaluation

This repository accompanies *Cross-Layer Evaluation and Fusion of Build-Time and Runtime Detection for Software Supply Chain Attacks*. It provides behavioral surrogates for seven SynthChain-inspired scenarios, Foreman and GoLeash experiment artifacts, the rule-based baseline, SCFusion stage-set evaluation, generated results.

## Repository layout

| Folder | Contents |
| --- | --- |
| `sc1_foreman_surrogate/`–`sc7_foreman_surrogate/` | Python surrogates, Foreman policies, and recorded build activity |
| `sc1_goleash_surrogate/`–`sc7_goleash_surrogate/` | Go surrogates, runtime policies, and recorded execution activity |
| `scfusion/` | Annotated stage inputs, set-union evaluator, reproducibility checks, and stage-attribution tables |
| `baseline/` | Artifact-name rules, archived artifact-inventory evaluation, and execution output |
| `results/` | Scenario summaries and comparison tables |
| `evidence_review/` | Additional analysis of stage attribution with supporting input and result tables |

## Requirements

- Python 3.9 or later for evaluation and tabulation (standard library).
- Foreman experiments require Python, the supplied build configurations, and a compatible execution environment.
- GoLeash experiments require Go and a Linux system supporting the tool's eBPF policy enforcement.

## Reproduce the stage-set calculations

Run these commands from the repository root:

```bash
python3 scfusion/scfusion.py
python3 scfusion/generate_paper_tables.py
python3 scfusion/validate_and_report.py
python3 -m unittest discover -s scfusion -p 'test_*.py'
```

`scfusion/stage_inputs.json` contains the archived stage assignments for each scenario. The scripts calculate per-scenario coverage, Foreman-only and GoLeash-only stages, overlap, stages reconstructed by neither detector, and macro-average coverage from exact fractions. SCFusion uses the **union of Foreman and GoLeash stage sets**; the baseline is evaluated separately. These commands calculate outcomes from archived annotations rather than running the two detector programs.

## Run the rule-based baseline

```bash
python3 baseline/run_baseline.py
```

The baseline matches configured artifact names to stage labels. The default inventory combines retained artifacts with archived Foreman file-creation records (`info.txt`) to account for generated files not retained in the folder snapshot. Its macro-average is **26.7%**. Because the default inventory incorporates Foreman activity records, it is not an independent detection sensor.

For a filesystem-snapshot-only comparison:

```bash
python3 baseline/run_baseline.py --snapshot-only
```

The snapshot-only macro-average is **20.2%**. The per-scenario rules and evidence-source records are in `baseline/scenarios.py` and `baseline/outputs/`.

## Evaluation interpretation

The original evaluation has 30 scenario-stage instances across seven scenarios, using detailed stages derived from the scenario descriptions. The benchmark's coarse evaluation taxonomy is different and should not be conflated with these labels.

The reported V1 results are derived from the saved stage assignments, and the accompanying event logs record what the detectors observed. Stage-attribution and evidence comparison data are provided in `scfusion/outputs/` and `evidence_review/` to distinguish stage-set arithmetic from raw detector observations. Detection of a local file operation is not in itself direct evidence of a network download or exfiltration.

## Reproducing detector observations

Each scenario folder contains its surrogate implementation and recorded output. Foreman policies are stored in `build_phases.json`, with observed file events in `info.txt` and permission warnings in `warnings.txt`. GoLeash scenario folders contain Go sources, policy artifacts, and execution logs. Rerunning those tools requires the corresponding platform, tool installation, and policies.

## Research context

SynthChain supplies scenario descriptions and ground-truth context. Foreman and GoLeash are separate research systems representing build-time monitoring and runtime policy enforcement respectively. SCFusion provides a common stage-set representation for this cross-layer comparison and evaluates the contribution of each source at the stage level.
