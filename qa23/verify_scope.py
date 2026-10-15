"""HF18 V5 bounded delta, 154 + 2 native sessions and inherited title/credits."""
from pathlib import Path
import csv,hashlib,json,os,struct,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import build,replace_checked
from tools.reference_bps.bps import apply
from qa15.inventory_layout import story_inventory
from qa18.scan_layout import scan

def sha(b):return hashlib.sha256(b).hexdigest()
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def main():
 jp=Path(os.environ.get('CONTINUITY_INPUT_JP',str(ROOT.parent/'jp_clean.ws'))).read_bytes()
 m=json.loads((ROOT/'manifest.json').read_text());rom,bps,result=build(jp)
 old=bytearray(jp);replace_checked(old,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits']);replace_checked(old,json.loads((ROOT/'docs/history/qa22/corrections_hf17.json').read_text())['edits']);old[-2:]=struct.pack('<H',sum(old[:-2])&65535);old=bytes(old)
 checks=0
 def ck(condition,label):
  nonlocal checks
  assert condition,label;checks+=1
 ck(sha(jp)==m['original']['sha256'],'clean JP');ck(sha(old)==m['previous_hf17']['sha256'],'HF17 pinned')
 ck(sha(rom)==m['target']['sha256'],'HF18 ROM');ck(apply(jp,bps)==rom,'Independent BPS')
 ck(bps==(ROOT/'patches/Chocobo_EN_v1.1_HF18_TEST_JP_CCAA4853.bps').read_bytes(),'Distributed BPS')
 ck(struct.unpack_from('<H',rom,len(rom)-2)[0]==sum(rom[:-2])&65535,'WS checksum')
 edits=json.loads((ROOT/'qa23/edits.json').read_text());allowed={len(rom)-2,len(rom)-1}
 for e in edits:
  off=int(e['offset'],16);before=bytes.fromhex(e['before']);after=bytes.fromhex(e['after']);end=off+len(before)
  ck(len(before)==len(after) and old[off:end]==before and rom[off:end]==after,e['id']);allowed.update(range(off,end))
 delta={i for i,(a,b) in enumerate(zip(old,rom))if a!=b};ck(delta<=allowed and len(delta)==m['changed_bytes_vs_hf17'],'Bounded delta')
 ck(old[0x160000:0x170000]==rom[0x160000:0x170000],'Font preserved')
 a,_=story_inventory(old,'HF17');b,_=story_inventory(rom,'HF18');a={x['id']:x for x in a};b={x['id']:x for x in b}
 tr=json.loads((ROOT/'qa23/translations.json').read_text());names=json.loads((ROOT/'qa23/name_reconciliation.json').read_text());alloc=json.loads((ROOT/'qa23/allocations.json').read_text())
 ck(len(a)==len(b)==3488 and len(tr)==65 and len(names)==2 and len(alloc)==65,'Story census')
 ck({id for id in a if a[id]['stream_sha256']!=b[id]['stream_sha256']}==set(tr)|set(names),'Only 67 resource streams changed')
 ck({id for id in a if a[id]['pointer']!=b[id]['pointer']}=={x['id']for x in alloc if x['mode']=='allocated'},'Only planned pointers')
 for id in set(tr)|set(names):ck(b[id]['terminated'] and b[id]['max_literal_cells']<=13,id+' width/termination')
 _,_,_,static=scan(rom);ck(static['story_unterminated']==static['getter_unterminated']==0,'Static termination')
 ids=json.loads((ROOT/'qa23/audit_ids.json').read_text());ck(len(ids)==154 and set(tr)<=set(ids),'V5 scope')
 frames=0;blank=0;visual=[];unchanged=0;nonblank=[]
 state=ROOT/'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss';driver=ROOT/'qa21/driver.lua'
 for id in ids+list(names):
  kind='G14' if id in ids else 'G09';r=ROOT/'evidence/qa23_runs'/('verified_'+id.replace(':','_'))
  meta=json.loads((r/'run.json').read_text());ck(meta['completed']and meta['exit']==0 and (r/'target_completed.txt').read_text().strip()=='true',id+' native completed')
  ck(meta['rom_sha256']==sha(rom) and meta['state_sha256']==sha(state.read_bytes()) and meta['script_sha256']==sha(driver.read_bytes()) and meta['mesen_sha256']==m['mesen_sha256'],id+' provenance')
  ck(meta['plan_sha256']==sha((r/'plan.lua').read_bytes()),id+' plan')
  story=[x for x in rows(r/'story.csv')if int(x['group'])==int(id[1:3]) and int(x['message'])==int(id[5:])]
  ck(any(x['event']=='read'and x['value']=='FFFF'and not(int(x['state'],16)&0x40)for x in story),id+' terminator')
  auto=[x for x in story if x['event']=='auto_line'];bad=[x for x in auto if x['value']!='0000'];nonblank.extend((id,x['value'])for x in bad);blank+=len(auto)-len(bad)
  ck(not bad,id+' no nonblank glyph dropped');ck((r/'sram.bin').stat().st_size==32768 and all(x['poweroff']=='false'for x in rows(r/'frames.csv')),id+' powered')
  frames+=int((r/'completed.txt').read_text().split('=')[1]);p=r/'end_text.png';ck(p.exists(),id+' image')
  visual.append({'id':id,'image':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'rom_sha256':sha(rom)})
  if id not in tr and id not in names:
   baseline=ROOT/'evidence/qa23_runs'/('baseline_'+id.replace(':','_'))/'end_text.png';ck(p.read_bytes()==baseline.read_bytes(),id+' exact pixels');unchanged+=1
 title_new=ROOT/'evidence/qa23_runs/final_title';title_old=ROOT/'evidence/qa14_runs/title_portable'
 nt=sorted(title_new.glob('anim*.png'));ot=sorted(title_old.glob('anim*.png'));ck(len(nt)==len(ot)==1001,'Title frame census')
 for x,y in zip(nt,ot):ck(x.name==y.name and x.read_bytes()==y.read_bytes(),x.name+' exact historical title')
 credits_new=ROOT/'evidence/qa23_runs/final_credits';credits_old=ROOT/'evidence/qa17_runs/final_credits'
 nc=sorted(credits_new.glob('credits_*.png'));oc=sorted(credits_old.glob('credits_*.png'));ck(len(nc)==len(oc)==14,'Credit page census')
 for x,y in zip(nc,oc):ck(x.name==y.name and x.read_bytes()==y.read_bytes(),x.name+' exact historical credits')
 for run in (title_new,credits_new):
  meta=json.loads((run/'run.json').read_text());ck(meta['completed'] and meta['exit']==0 and meta['rom_sha256']==sha(rom),run.name+' native HF18 provenance')
 result.update({'status':'V5_EXECUTED_SCOPED_WITH_LEXICAL_RESERVES','checks':checks,'references_reviewed':len(ids),'references_changed':len(tr),'name_reconciliations':len(names),'native_sessions_final':len(visual),'story_terminators_reached':len(visual),'native_frames':frames,'native_end_images':len(visual),'nonblank_dropped_glyphs':nonblank,'blank_padding_drops':blank,'unchanged_exact_end_images':unchanged,'title_frames_exact_historical':len(nt),'credit_pages_exact_historical':len(nc),'changed_bytes_vs_hf17':len(delta),'independent_bps':'PASS_EXACT_BYTES','global_visual_approved':False,'global_linguistic_approved':False,'natural_reachability':'NOT_VALIDATED','static':static})
 (ROOT/'qa23/visual_readings.json').write_text(json.dumps(visual,indent=2)+'\n');(ROOT/'qa23/verification.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ('status','checks','references_reviewed','references_changed','name_reconciliations','native_sessions_final','native_frames','unchanged_exact_end_images','title_frames_exact_historical','credit_pages_exact_historical')},indent=2))
if __name__=='__main__':main()
