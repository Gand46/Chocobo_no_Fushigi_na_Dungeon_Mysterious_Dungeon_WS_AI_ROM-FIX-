"""Clean extraction gate: canonical BPS plus independent editable regeneration."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import build,PATCH_NAME
base=Path(os.environ['CONTINUITY_INPUT_JP']);out=ROOT/'build';out.mkdir(exist_ok=True)
rom,bps,report=build(base.read_bytes())
(out/'Chocobo_EN_v1.1_HF15_TEST.ws').write_bytes(rom);(out/PATCH_NAME).write_bytes(bps)
subprocess.run([sys.executable,str(ROOT/'qa20/rebuild_translation_edits.py'),'--japanese-rom',str(base),'--out',str(out/'semantic')],check=True)
assert (out/'semantic/candidate.ws').read_bytes()==rom
assert json.loads((out/'semantic/edits.json').read_text())==json.loads((ROOT/'qa20/edits.json').read_text())
report['editable_regeneration']='PASS_EXACT_ROM_AND_EDITS'
(out/'release_build_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
