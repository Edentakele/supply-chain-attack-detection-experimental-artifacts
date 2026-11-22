"""Reproduce V1 from unchanged stage assignments; flag unverified detector-stage claims.

This is a provenance and arithmetic audit, NOT automated detector-to-stage normalization.
"""
from pathlib import Path
from collections import Counter
import csv
import json
import argparse

ROOT = Path(__file__).resolve().parent
FIELDS = ("scenario", "detector", "stage")

def compute(inputs):
    results = {}
    for scenario, row in inputs.items():
        gt = row["ground_truth"]
        if not gt or len(gt) != len(set(gt)):
            raise ValueError(f"{scenario}: ground truth must be nonempty and unique")
        g = set(gt)
        f, l = set(row["foreman"]), set(row["goleash"])
        for tool in ("foreman", "goleash"):
            if len(row[tool]) != len(set(row[tool])):
                raise ValueError(f"{scenario}: duplicate stages in {tool}")
        if not (f | l) <= g:
            raise ValueError(f"{scenario}: detected stages outside ground truth")
        both = f & l
        union = f | l
        if len(union) != len(f) + len(l) - len(both):
            raise AssertionError("set union invariant")
        results[scenario] = {
            "total_stages": len(g),
            "foreman_stages": sorted(f), "goleash_stages": sorted(l),
            "overlap_stages": sorted(both), "overlap_count": len(both),
            "fused_stages": sorted(union), "missing_stages": sorted(g-union),
            "foreman_percent": 100*len(f)/len(g),
            "goleash_percent": 100*len(l)/len(g),
            "scfusion_percent": 100*len(union)/len(g),
        }
    return results

def validate_evidence(inputs, audit):
    expected = {(sc,tool,stage) for sc, row in inputs.items() for tool in ("foreman","goleash") for stage in row[tool]}
    seen = set(); unverified=[]; invalid=[]
    for row in audit:
        key=tuple(row[field] for field in FIELDS)
        if key not in expected or key in seen:
            invalid.append(key)
        seen.add(key)
        status=row["verification_status"].strip().lower()
        if status != 'verified' or not all(row[k].strip() for k in ('evidence_file','evidence_excerpt','mapping_rationale')):
            unverified.append(key)
        if status == 'verified':
            file_path = (ROOT.parent / row['evidence_file']).resolve()
            if not file_path.is_relative_to(ROOT.parent.resolve()) or not file_path.is_file():
                invalid.append(key)
            elif row['evidence_excerpt'] not in file_path.read_text(errors='replace'):
                invalid.append(key)
    missing=expected-seen
    if missing or invalid:
        raise ValueError(f"Evidence rows missing={sorted(missing)} invalid={sorted(invalid)}")
    return unverified

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--require-verified',action='store_true',help='fail unless each credit has reviewed supporting evidence')
    args=p.parse_args()
    inputs=json.loads((ROOT/'stage_inputs.json').read_text())
    with (ROOT/'stage_evidence_audit.csv').open(newline='') as h: audit=list(csv.DictReader(h))
    results=compute(inputs)
    unverified=validate_evidence(inputs,audit)
    out=ROOT/'outputs'
    out.mkdir(exist_ok=True)
    (out/'v1_reproduction_audit.json').write_text(json.dumps({'results':results,'unverified_detector_stage_credits':len(unverified),'verification_status':'unverified' if unverified else 'reviewed'},indent=2)+'\n')
    with (out/'v1_reproduction_audit.csv').open('w',newline='') as h:
        w=csv.writer(h)
        w.writerow(['scenario','ground_truth_count','foreman_percent','goleash_percent','scfusion_percent','overlap_count','overlap_stages','status'])
        for sc,r in results.items():
            w.writerow([sc,r['total_stages'],f"{r['foreman_percent']:.4f}",f"{r['goleash_percent']:.4f}",f"{r['scfusion_percent']:.4f}",r['overlap_count'],'; '.join(r['overlap_stages']),'UNVERIFIED' if unverified else 'REVIEWED'])
    for sc,r in results.items():
        print(f"{sc}: F={r['foreman_percent']:.1f}%, G={r['goleash_percent']:.1f}%, fusion={r['scfusion_percent']:.1f}% overlap={r['overlap_count']}")
    print(f"Unverified credits: {len(unverified)} of {len(audit)}")
    if args.require_verified and unverified:
        raise SystemExit('Evidence verification incomplete; results cannot be treated as validated.')

if __name__=='__main__':main()
