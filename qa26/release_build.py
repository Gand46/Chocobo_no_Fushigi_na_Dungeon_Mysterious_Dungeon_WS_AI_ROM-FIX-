"""Rebuild HF20 from JP and regenerate the aesthetic edits independently."""
from pathlib import Path
import json,os,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import build,PATCH_NAME
from qa26.rebuild_edits import baseline,repair
jp=Path(os.environ['CONTINUITY_INPUT_JP']).read_bytes()
rom,bps,result=build(jp)
semantic,edits,review=repair(baseline(jp))
assert semantic==rom
assert edits==json.loads((ROOT/'qa26/edits.json').read_text())
assert review==json.loads((ROOT/'qa26/layout_review.json').read_text())
assert bps==(ROOT/'patches'/PATCH_NAME).read_bytes()
out=ROOT/'build';out.mkdir(exist_ok=True)
(out/'Chocobo_EN_v1.1_HF20_TEST.ws').write_bytes(rom)
(out/PATCH_NAME).write_bytes(bps)
result['editable_regeneration']='PASS_EXACT_ROM_EDITS_AND_REVIEW'
(out/'release_build_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
