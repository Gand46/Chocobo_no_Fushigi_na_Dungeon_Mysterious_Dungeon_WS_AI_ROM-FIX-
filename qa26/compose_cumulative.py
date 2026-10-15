"""Fold HF19→HF20 edits into the single legacy→HF20 checked recipe."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
old=json.loads((ROOT/'docs/history/qa25/corrections_hf19.json').read_text())['edits']
new=json.loads((ROOT/'qa26/edits.json').read_text())
combined=json.loads(json.dumps(old));merged=[]
for n in new:
 start=int(n['offset'],16);before=bytes.fromhex(n['before']);after=bytes.fromhex(n['after']);end=start+len(before)
 hits=[o for o in combined if start<int(o['offset'],16)+len(bytes.fromhex(o['after'])) and int(o['offset'],16)<end]
 if not hits:
  combined.append(n);continue
 assert len(hits)==1,(n['id'],len(hits));o=hits[0];ostart=int(o['offset'],16);original=bytearray.fromhex(o['after']);rel=start-ostart
 assert 0<=rel and rel+len(before)<=len(original),(n['id'],o['id'])
 assert original[rel:rel+len(before)]==before,(n['id'],o['id'],'mismatched sequential preimage')
 original[rel:rel+len(after)]=after;o['after']=original.hex();o['reason']+=' [QA26 '+n['id']+': '+n['reason']+']';merged.append({'new':n['id'],'into':o['id']})
(ROOT/'src/corrections.json').write_text(json.dumps({'edits':combined},ensure_ascii=False,indent=2)+'\n')
(ROOT/'qa26/cumulative_merges.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n')
print('merged',merged,'total canonical edits',len(combined))
