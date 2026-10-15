"""Verify the HF17 V4 resource delta and all 194 final native G09 sessions."""
from pathlib import Path
import csv, hashlib, json, struct, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build import build
from tools.reference_bps.bps import apply
from qa15.inventory_layout import story_inventory
from qa18.scan_layout import scan
from qa22.hf16_base import input_path,reconstruct

def sha(data):return hashlib.sha256(data).hexdigest()
def rows(path):
 with path.open() as f:return list(csv.DictReader(f))

def main():
 jp=input_path().read_bytes();rom,bps,result=build(jp)
 m=json.loads((ROOT/'manifest.json').read_text());old=reconstruct(jp)
 checks=0
 def ck(condition,label):
  nonlocal checks
  assert condition,label
  checks+=1
 ck(sha(old)==m['previous_hf16']['sha256'],'HF16 baseline')
 ck(sha(rom)==m['target']['sha256'],'HF17 ROM')
 ck(apply(jp,bps)==rom,'Independent BPS direct JP')
 ck(bps==(ROOT/'patches/Chocobo_EN_v1.1_HF17_TEST_JP_CCAA4853.bps').read_bytes(),'Distributed BPS exact')
 ck(struct.unpack_from('<H',rom,len(rom)-2)[0]==sum(rom[:-2])&65535,'WonderSwan checksum')
 edits=json.loads((ROOT/'qa22/edits.json').read_text());allowed={len(rom)-2,len(rom)-1}
 for e in edits:
  off=int(e['offset'],16);before=bytes.fromhex(e['before']);after=bytes.fromhex(e['after']);end=off+len(before)
  ck(len(before)==len(after) and old[off:end]==before and rom[off:end]==after,e['id'])
  allowed.update(range(off,end))
 delta={i for i,(a,b) in enumerate(zip(old,rom))if a!=b}
 ck(delta<=allowed and len(delta)==m['changed_bytes_vs_hf16'],'Bounded HF17 delta')
 ck(old[0x160000:0x170000]==rom[0x160000:0x170000],'Shared font unchanged')
 old_story,_=story_inventory(old,'HF16');new_story,_=story_inventory(rom,'HF17')
 a={r['id']:r for r in old_story};b={r['id']:r for r in new_story}
 tr=json.loads((ROOT/'qa22/translations.json').read_text());allocation=json.loads((ROOT/'qa22/allocations.json').read_text())
 ck(len(a)==len(b)==3488 and len(tr)==43 and len(allocation)==43,'Story census and edits')
 ck({id for id in a if a[id]['stream_sha256']!=b[id]['stream_sha256']}==set(tr),'Only planned G09 streams changed')
 ck({id for id in a if a[id]['pointer']!=b[id]['pointer']}=={r['id']for r in allocation if r['mode']=='allocated'},'Only planned pointers changed')
 for id in tr:ck(b[id]['terminated'] and b[id]['max_literal_cells']<=13,id+' termination/width')
 _,_,_,static=scan(rom)
 ck(static['story_unterminated']==static['getter_unterminated']==0,'No unterminated text in census')
 ids=json.loads((ROOT/'qa22/audit_ids.json').read_text());ck(len(ids)==194 and set(tr)<=set(ids),'V4 scope')
 frames=0;blank=0;nonblank=[];visual=[];unchanged_pixels=[]
 state=ROOT/'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss'
 driver=ROOT/'qa21/driver.lua'
 for id in ids:
  name=id.replace(':','_');r=ROOT/'evidence/qa22_runs'/('verified_'+name);baseline=ROOT/'evidence/qa22_runs'/('baseline_'+name)
  meta=json.loads((r/'run.json').read_text());ck(meta['completed']and meta['exit']==0 and (r/'target_completed.txt').read_text().strip()=='true',id+' native completion')
  ck(meta['rom_sha256']==sha(rom) and meta['state_sha256']==sha(state.read_bytes()) and meta['script_sha256']==sha(driver.read_bytes()) and meta['mesen_sha256']==m['mesen_sha256'],id+' native provenance')
  ck(meta['plan_sha256']==sha((r/'plan.lua').read_bytes()),id+' plan')
  story=[x for x in rows(r/'story.csv')if int(x['group'])==9 and int(x['message'])==int(id[5:])]
  ck(any(x['event']=='read'and x['value']=='FFFF'and not(int(x['state'],16)&0x40)for x in story),id+' text terminator')
  auto=[x for x in story if x['event']=='auto_line'];bad=[x for x in auto if x['value']!='0000']
  if bad:nonblank.append({'id':id,'count':len(bad)})
  blank+=len(auto)-len(bad)
  ck(not bad,id+' no nonblank dropped glyph')
  ck((r/'sram.bin').stat().st_size==32768 and all(x['poweroff']=='false'for x in rows(r/'frames.csv')),id+' powered native run')
  frames+=int((r/'completed.txt').read_text().split('=')[1])
  pages=sorted(r.glob('page_*.png'))
  ck(bool(pages),id+' image evidence')
  for image in pages:
   visual.append({'id':id,'run':r.name,'image':image.name,'sha256':sha(image.read_bytes())})
  if id not in tr:
   native_baseline=sorted(baseline.glob('page_*.png'))
   unchanged_pixels.append({'id':id,'exact_page_images':len(native_baseline)==len(pages) and all(x.read_bytes()==y.read_bytes() for x,y in zip(native_baseline,pages))})
 ck(all(x['exact_page_images']for x in unchanged_pixels),'Unchanged V4 scenes exact baseline pixels')
 result.update({'status':'V4_EXECUTED_SCOPED_WITH_TWO_NAME_RESERVES','checks':checks,'references_reviewed':len(ids),'references_changed':len(tr),'native_sessions_final':len(ids),'story_terminators_reached':len(ids),'native_frames':frames,'native_page_images':len(visual),'nonblank_dropped_glyphs':nonblank,'blank_padding_drops':blank,'unchanged_exact_page_images':sum(x['exact_page_images']for x in unchanged_pixels),'changed_bytes_vs_hf16':len(delta),'independent_bps':'PASS_EXACT_BYTES','global_visual_approved':False,'global_linguistic_approved':False,'natural_reachability':'NOT_VALIDATED','static':static})
 (ROOT/'qa22/visual_readings.json').write_text(json.dumps(visual,indent=2)+'\n')
 (ROOT/'qa22/verification.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({key:result[key] for key in ('status','checks','references_reviewed','references_changed','native_sessions_final','story_terminators_reached','native_frames','native_page_images','blank_padding_drops','unchanged_exact_page_images')},indent=2))

if __name__=='__main__':main()
