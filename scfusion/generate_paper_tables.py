"""Generate original V1 stage-score and attribution tables from unchanged stage inputs.
The results are conditional on legacy preassigned stages; not independent detector validation.
"""
from pathlib import Path
from fractions import Fraction
import csv,json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from baseline.scenarios import SCENARIOS
inputs=json.loads((ROOT/'stage_inputs.json').read_text())
keys=['foreman','goleash','baseline','scfusion']; sums={k:Fraction(0) for k in keys}
with (ROOT/'outputs'/'fraction_accurate_coverage.csv').open('w',newline='') as f, (ROOT/'outputs'/'stage_attribution.csv').open('w',newline='') as a:
 w=csv.writer(f);u=csv.writer(a)
 w.writerow(['scenario','ground_truth_count',*[k+'_fraction' for k in keys],*[k+'_percent' for k in keys]])
 u.writerow(['scenario','foreman_only','goleash_only','both','neither','unique_F','unique_G','overlap','missed'])
 for sid,p in inputs.items():
  E=set(p['ground_truth']);F=set(p['foreman']);G=set(p['goleash']);B=set(SCENARIOS[sid]['rules'].values())&E
  d={'foreman':Fraction(len(F),len(E)),'goleash':Fraction(len(G),len(E)),'baseline':Fraction(len(B),len(E)),'scfusion':Fraction(len(F|G),len(E))}
  for k in keys:sums[k]+=d[k]
  w.writerow([sid,len(E),*[str(d[k]) for k in keys],*[f'{float(d[k]*100):.4f}' for k in keys]])
  fmt=lambda s:'; '.join(sorted(s))
  u.writerow([sid,fmt(F-G),fmt(G-F),fmt(F&G),fmt(E-F-G),len(F-G),len(G-F),len(F&G),len(E-F-G)])
 w.writerow(['MACRO_AVERAGE',sum(len(v['ground_truth']) for v in inputs.values()),*[str(sums[k]/len(inputs)) for k in keys],*[f'{float(sums[k]*100/len(inputs)):.4f}' for k in keys]])
print('V1 original-stage macro averages:', {k:round(float(sums[k]*100/len(inputs)),3) for k in keys})
