"""Run the artifact-name baseline with auditable provenance.

Default uses retained files plus created-file entries from archived Foreman
info.txt, because some generated files are absent from the released snapshot.
Use --snapshot-only to score retained files alone.
"""
from pathlib import Path
from fractions import Fraction
import argparse, csv, json
from baseline import evaluate_scenario
from scenarios import SCENARIOS

parser=argparse.ArgumentParser()
parser.add_argument('--snapshot-only',action='store_true',help='Ignore archived file creation evidence')
args=parser.parse_args()
root=Path(__file__).resolve().parent
outputs=root/'outputs'; outputs.mkdir(exist_ok=True)
results={}
for scenario,config in SCENARIOS.items():
    results[scenario]=evaluate_scenario(root,config,not args.snapshot_only)
mode='snapshot' if args.snapshot_only else 'archived_artifact_inventory'
with (outputs/f'baseline_results_{mode}.json').open('w') as f:
    json.dump(results,f,indent=2);f.write('\n')
with (outputs/f'baseline_results_{mode}.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['scenario','stages','detected','matched_artifact','provenance','fraction','coverage_pct'])
    for sid,res in results.items():
        w.writerow([sid,len(res['ground_truth']),'; '.join(res['detected']),
                    '; '.join(m['artifact'] for m in res['matched_rules']),
                    '; '.join(src['source'] for m in res['matched_rules'] for src in m['sources']),
                    f"{len(res['detected'])}/{len(res['ground_truth'])}",res['exact_coverage']])
mean=sum((Fraction(len(r['detected']),len(r['ground_truth'])) for r in results.values()),Fraction(0))/len(results)
print('mode:',mode)
for sid,res in results.items():
    print(sid, f"{len(res['detected'])}/{len(res['ground_truth'])}",f"{res['exact_coverage']:.2f}%",'; '.join(res['detected']))
print(f'macro-average: {float(mean*100):.4f}% (round to {float(mean*100):.1f}%)')
