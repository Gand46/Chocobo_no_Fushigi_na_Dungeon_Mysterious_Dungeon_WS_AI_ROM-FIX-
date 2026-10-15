"""Verify QA24 binary scope, native traces, provenance and cumulative BPS."""
from pathlib import Path
import csv,hashlib,json,os,struct,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import build
from qa24.rebuild_translation_edits import reconstruct
from qa15.inventory_layout import story_inventory,getter_inventory
from tools.reference_bps.bps import apply
sha=lambda b:hashlib.sha256(b).hexdigest()
def csvrows(p):
 with p.open() as f:return list(csv.DictReader(f))
def main():
 checks=0
 def ck(v,label):
  nonlocal checks
  assert v,label;checks+=1
 jp=Path(os.environ['CONTINUITY_INPUT_JP']).read_bytes();old=reconstruct(jp);rom,bps,result=build(jp)
 m=json.loads((ROOT/'manifest.json').read_text());edits=json.loads((ROOT/'qa24/edits.json').read_text());allowed={len(rom)-2,len(rom)-1}
 for e in edits:
  off=int(e['offset'],16);before=bytes.fromhex(e['before']);after=bytes.fromhex(e['after'])
  ck(old[off:off+len(before)]==before and rom[off:off+len(after)]==after,e['id']);allowed.update(range(off,off+len(after)))
 diff={i for i,(a,b)in enumerate(zip(old,rom))if a!=b};ck(diff<=allowed and len(diff)==97,'97 bounded changed bytes')
 ck(apply(jp,bps)==rom,'Independent BPS roundtrip');ck(bps==(ROOT/'patches/Chocobo_EN_v1.1_HF19_TEST_JP_CCAA4853.bps').read_bytes(),'Delivered BPS')
 ck(struct.unpack_from('<H',rom,len(rom)-2)[0]==sum(rom[:-2])&65535,'WS checksum')
 ck(old[0x140000:0x190000]==rom[0x140000:0x190000],'All code/font banks14..18 preserved')
 a={x['id']:x for x in story_inventory(old,'HF18')[0]};b={x['id']:x for x in story_inventory(rom,'HF19')[0]}
 ck(len(a)==len(b)==3488,'story count');ck({i for i in a if a[i]['stream_sha256']!=b[i]['stream_sha256']}=={'G00:M253','G06:M100','G11:M011','G16:M073'},'four story streams changed')
 ck({i for i in a if a[i]['pointer']!=b[i]['pointer']}=={'G11:M011','G16:M073'},'two shared suffix pointers')
 a={x['id']:x for x in getter_inventory(old,'HF18')[0]};b={x['id']:x for x in getter_inventory(rom,'HF19')[0]}
 ck(len(a)==len(b)==2333,'getter count');ck({i for i in a if a[i]['stream_sha256']!=b[i]['stream_sha256']}=={'F17:I067','F17:I152'},'two getter streams changed')
 ck(all(x['terminated']for x in b.values()),'getter termination')
 sessions=[];frames=0;blank=0
 for r in sorted((ROOT/'evidence/qa24_runs').glob('final_*')):
  meta=json.loads((r/'run.json').read_text());ck(meta['completed']and meta['exit']==0,r.name+' completion')
  ck(meta['rom_sha256']==sha(rom)and meta['mesen_sha256']==m['mesen_sha256'],r.name+' provenance')
  ck(meta['plan_sha256']==sha((r/'plan.lua').read_bytes()),r.name+' plan')
  ck((r/'target_completed.txt').read_text().strip()=='true',r.name+' target terminator')
  rows=csvrows(r/'story.csv');bad=[x for x in rows if x['event']=='auto_line'and x['value']!='0000'];ck(not bad,r.name+' no nonblank discarded')
  blank+=sum(x['event']=='auto_line'and x['value']=='0000'for x in rows)
  ck(any(x['value']=='FFFF'and x['event']=='read' for x in rows),r.name+' native FFFF')
  frames+=int((r/'completed.txt').read_text().split('=')[1]);imgs=sorted(r.glob('page_*.png'))or[r/'end_text.png']
  for p in imgs:ck(p.is_file(),r.name+' image')
  sessions.append({'run':r.name,'access_method':'POINTER_INJECTION + WRAM_POKE where dynamic','images':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes())}for p in imgs]})
 ck(len(sessions)==20,'twenty text sessions')
 for name,index in [('bestiary_treant_scroll',7),('bestiary_omega',152),('bestiary_ruin_fixture',67)]:
  r=ROOT/'evidence/qa24_runs'/name;meta=json.loads((r/'run.json').read_text())
  ck(meta['completed']and meta['exit']==0 and meta['rom_sha256']==sha(rom),name+' native')
  ck(meta['plan_sha256']==sha((r/'plan.lua').read_bytes()),name+' plan')
  got=[x for x in csvrows(r/'getters.csv')if int(x['family'])==17 and int(x['index'])==index and int(x['window'])==129]
  ck(got and any(x['value']=='FFFF'for x in got),name+' F17 consumer terminator')
  stores=[x for x in csvrows(r/'stores.csv')if int(x['family'])==17 and int(x['index'])==index]
  ck(stores and not any(x['row_overflow']=='true'for x in stores),name+' row bounds')
  p=r/'f00120.png';ck(p.is_file(),name+' image');frames+=600
  sessions.append({'run':name,'access_method':'SYNTHETIC_STATE; preset81 and monster selection; Ruin overrides skill index','images':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes())}]})
 result.update(status='PASS_SCOPED_QA24',checks=checks,story_sessions=20,bestiary_sessions=3,native_sessions_final=23,native_frames=frames,changed_story_resources=4,changed_getter_resources=2,changed_bytes_vs_hf18=len(diff),nonblank_dropped_glyphs=0,blank_padding_drops=blank,independent_bps='PASS_EXACT_BYTES',global_visual_approved=False,global_linguistic_approved=False,natural_reachability='NOT_VALIDATED',sessions=sessions)
 (ROOT/'qa24/verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='sessions'},indent=2))
if __name__=='__main__':main()
