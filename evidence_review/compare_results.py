#!/usr/bin/env python3
"""Reproduce historical versus evidence-screened stage coverage (no detector execution)."""
from pathlib import Path
from fractions import Fraction
import json,csv
root=Path(__file__).resolve().parent.parent
original=json.loads((root/'scfusion'/'stage_inputs.json').read_text())
screened=json.loads((root/'evidence_review'/'evidence_screened_stage_inputs.json').read_text())
assert original.keys()==screened.keys()
rows=[];totals=[Fraction(0)]*6
for sid in original:
 o=original[sid]; n=screened[sid]; E=set(o['ground_truth']); assert E==set(n['ground_truth'])
 vals=[]
 for data in (o,n):
  F=set(data['foreman']);G=set(data['goleash']);assert (F|G)<=E
  vals.append([Fraction(len(x),len(E)) for x in (F,G,F|G)])
 ovals,nvals=vals
 ordered=[ovals[0],nvals[0],ovals[1],nvals[1],ovals[2],nvals[2]]
 totals=[v+x for v,x in zip(totals,ordered)]
 rows.append((sid,len(E),*[f'{float(v*100):.4f}' for v in ordered]))
headers=['scenario','stages','original_foreman','screened_foreman','original_goleash','screened_goleash','original_fusion','screened_fusion']
with (root/'evidence_review'/'original_vs_evidence_screened.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(headers);w.writerows(rows)
 w.writerow(['MACRO_AVERAGE',sum(len(v['ground_truth']) for v in original.values()),*[f'{float(v*100/len(original)):.4f}' for v in totals]])
print('Original vs evidence-screened macro averages:')
for i,k in enumerate(headers[2:]):print(f'{k}: {float(totals[i]*100/len(original)):.2f}%')
