# Reproduction commands

From the repository root, with Python 3.9 or later:

```bash
python3 scfusion/scfusion.py
python3 scfusion/generate_paper_tables.py
python3 scfusion/validate_and_report.py
python3 baseline/run_baseline.py
python3 -m unittest discover -s scfusion -p 'test_*.py'
```

Stage assignments are read from `scfusion/stage_inputs.json`; source observations are in the scenario log directories. Generated coverage and attribution tables are in `scfusion/outputs/`. The baseline rules are in `baseline/scenarios.py` and generated results in `baseline/outputs/`.

Use `python3 baseline/run_baseline.py --snapshot-only` to compare against retained filesystem artifacts without consulting archived file-creation events.
