import unittest
import json
from pathlib import Path
from validate_and_report import compute

class ReproductionTests(unittest.TestCase):
    def test_original_v1_scores_and_overlap(self):
        data=json.loads((Path(__file__).resolve().parent/'stage_inputs.json').read_text())
        results=compute(data)
        expected={
          'SC1':(50,25,75,0),'SC2':(100/3,100/3,200/3,0),
          'SC3':(20,40,60,0),'SC4':(50,25,50,1),
          'SC5':(25,50,75,0),'SC6':(50,25,50,1),
          'SC7':(100/3,100/3,200/3,0)}
        for sc,(f,g,union,overlap) in expected.items():
            self.assertAlmostEqual(results[sc]['foreman_percent'],f)
            self.assertAlmostEqual(results[sc]['goleash_percent'],g)
            self.assertAlmostEqual(results[sc]['scfusion_percent'],union)
            self.assertEqual(results[sc]['overlap_count'],overlap)
    def test_unknown_stages_rejected(self):
        with self.assertRaises(ValueError):
            compute({'SC1':{'ground_truth':['A'],'foreman':['B'],'goleash':[]}})

if __name__=='__main__':unittest.main()
