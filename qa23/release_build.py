"""Clean-extraction HF18: cumulative checked recipe and editable V5 regeneration."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import build,PATCH_NAME
jp=Path(os.environ['CONTINUITY_INPUT_JP']);out=ROOT/'build';out.mkdir(exist_ok=True)
rom,bps,result=build(jp.read_bytes());(out/'Chocobo_EN_v1.1_HF18_TEST.ws').write_bytes(rom);(out/PATCH_NAME).write_bytes(bps)
semantic=out/'semantic'
subprocess.run([sys.executable,str(ROOT/'qa23/rebuild_translation_edits.py'),'--japanese-rom',str(jp),'--out',str(semantic)],check=True)
assert (semantic/'candidate.ws').read_bytes()==rom
assert json.loads((semantic/'edits.json').read_text())==json.loads((ROOT/'qa23/edits.json').read_text())
assert (ROOT/'patches'/PATCH_NAME).read_bytes()==bps
result['editable_regeneration']='PASS_EXACT_ROM_AND_EDITS';(out/'release_build_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
