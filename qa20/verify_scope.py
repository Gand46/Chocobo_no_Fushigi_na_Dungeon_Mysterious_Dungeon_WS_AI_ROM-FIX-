"""Verify HF15 bytes, resource scope and final native evidence; scoped, not global QA."""
from pathlib import Path
import argparse,csv,hashlib,json,struct,sys
ROOT=Path(__file__).resolve().parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();sys.path.insert(0,str(ROOT))
 from build import build
 from tools.reference_bps.bps import apply
 from qa15.inventory_layout import story_inventory,getter_inventory
 from qa18.scan_layout import scan
 m=json.loads((ROOT/'docs/history/qa20/manifest.json').read_text());jp=args.japanese_rom.read_bytes();bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF15_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(jp,bps);b={'scope':'HISTORICAL_HF15'}
 old=apply(jp,(ROOT/'patches/historical/Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps').read_bytes());checks=0
 def ck(v,label):
  nonlocal checks
  assert v,label;checks+=1
 ck(sha(old)==m['previous_hf14']['sha256'],'HF14 authority');ck(apply(jp,bps)==rom,'Independent BPS exact');ck(sha(bps)==m['bps_sha256'],'BPS hash');ck(sha(rom)==m['target']['sha256'],'HF15 hash');ck(len(rom)==len(old)==2097152,'ROM size');ck(sum(rom[:-2])&65535==struct.unpack('<H',rom[-2:])[0],'Checksum')
 edits=json.loads((ROOT/'qa20/edits.json').read_text());allowed={len(rom)-2,len(rom)-1}
 for e in edits:
  x=int(e['offset'],16);before=bytes.fromhex(e['before']);after=bytes.fromhex(e['after']);y=x+len(after)
  ck(len(before)==len(after),'Same extent');ck(old[x:y]==before,'HF14 preimage');ck(rom[x:y]==after,'HF15 payload');allowed.update(range(x,y))
 changed={i for i,(x,y)in enumerate(zip(old,rom))if x!=y};ck(changed<=allowed,'No unlisted changes');ck(len(changed)==4279,'Delta count');ck(old[0x1bdcd0:0x1c0000]==jp[0x1bdcd0:0x1c0000]==b'\xff'*(0x1c0000-0x1bdcd0),'Original and HF14 free space');ck(rom[0x160000:0x170000]==old[0x160000:0x170000],'Font unchanged')
 st0,_=story_inventory(old,'HF14');st1,_=story_inventory(rom,'HF15');a0={x['id']:x for x in st0};a1={x['id']:x for x in st1};tr=json.loads((ROOT/'qa20/translations.json').read_text());ck(len(st0)==len(st1)==3488,'Story census');ck(set(a0)==set(a1),'Story identities');ck({x for x in a0 if a0[x]['stream_sha256']!=a1[x]['stream_sha256']}==set(tr),'Only 74 streams changed');ck({x for x in a0 if a0[x]['pointer']!=a1[x]['pointer']}==set(tr),'Only 74 bindings changed');ck(len(tr)==74,'Corrections')
 for id in tr:ck(a1[id]['terminated'],id+' terminated');ck(a1[id]['max_literal_cells']<=13,id+' width');ck(a0[id]['bank']==a1[id]['bank']==27,id+' bank')
 g0,_=getter_inventory(old,'HF14');g1,_=getter_inventory(rom,'HF15');ck([(x['id'],x['pointer'],x['stream_sha256'])for x in g0]==[(x['id'],x['pointer'],x['stream_sha256'])for x in g1],'Getter bytes and bindings unchanged');_,_,_,summary=scan(rom);ck(summary['story_unterminated']==summary['getter_unterminated']==0,'No unterminated streams')
 ids=json.loads((ROOT/'qa20/audit_ids.json').read_text());review=json.loads((ROOT/'qa20/linguistic_review.json').read_text());reserve={x['id']for x in review if x['status']=='NEEDS_CONTEXT'};frames=0;blank=0;nonblank=[];incomplete=[];getrows=lambda p:list(csv.DictReader(p.open()))
 for id in ids:
  r=ROOT/'evidence/qa20_runs'/('release_'+id.replace(':','_'));meta=json.loads((r/'run.json').read_text());ck(meta['completed']and meta['exit']==0,id+' completed');
  target=(r/'target_completed.txt').read_text()=='true'
  if not target:incomplete.append(id)
  if id not in reserve:ck(target,id+' target reached')
  ck(meta['rom_sha256']==m['target']['sha256'],id+' ROM');ck(meta['script_sha256']==sha((ROOT/'qa20/driver.lua').read_bytes()),id+' driver');ck(meta['plan_sha256']==sha((r/'plan.lua').read_bytes()),id+' plan');ck(meta['state_sha256']==sha((ROOT/'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss').read_bytes()),id+' initial state');ck(not(r/'dump_error.txt').exists(),id+' no dump error');ck((r/'sram.bin').stat().st_size==32768,id+' SRAM');ck(all(x['poweroff']=='false'for x in getrows(r/'frames.csv')),id+' powered')
  group=int(id[1:3]);msg=int(id[5:]);story=[x for x in getrows(r/'story.csv')if int(x['group'])==group and int(x['message'])==msg];
  if id not in reserve:ck(any(x['event']=='read'and x['value']=='FFFF'and not(int(x['state'],16)&0x40)for x in story),id+' terminator')
  auto=[x for x in story if x['event']=='auto_line'];bad=[x for x in auto if x['value']!='0000'];blank+=len(auto)-len(bad)
  if bad:nonblank.append({'id':id,'count':len(bad),'status':'EXCLUDED_CONTEXT_DIAGNOSTIC'})
  if id not in reserve:ck(not bad,id+' no nonblank glyph discarded')
  frames+=int((r/'completed.txt').read_text().split('=')[1])
 vis=json.loads((ROOT/'qa20/visual_readings.json').read_text())
 for x in vis:ck(sha((ROOT/'evidence/qa20_runs'/x['run']/x['image']).read_bytes())==x['sha256'],'Visual evidence hash')
 for name in ['release_menu_empty','release_menu_saved','release_save_native','release_load_saved']:
  r=ROOT/'evidence/qa20_runs'/name;meta=json.loads((r/'run.json').read_text());ck(meta['rom_sha256']==m['target']['sha256']and meta['exit']==0 and meta['completed'],name+' final native session');frames+=int((r/'completed.txt').read_text().split('=')[1])
 ck(len(ids)==len(review)==248,'V2 coverage');ck(len(reserve)==6,'Context reserves');ck(sum(x['status']=='PASS_SYNTHETIC_REVIEWED_SCOPED'for x in review)==242,'Scoped approvals')
 result={'status':'V2_EXECUTED_SCOPED_WITH_SIX_CONTEXT_RESERVES','checks':checks,'references_reviewed':248,'references_changed':74,'scoped_pass':242,'context_pending':sorted(reserve),'native_sessions_final':252,'story_terminators_reached':248-len(incomplete),'incomplete_excluded_diagnostics':incomplete,'native_frames':frames,'visual_readings':len(vis),'approved_nonblank_dropped_glyphs':0,'blank_padding_drops':blank,'excluded_diagnostics':nonblank,'changed_bytes_vs_hf14':len(changed),'independent_bps':'PASS_EXACT_BYTES','global_visual_approved':False,'global_linguistic_approved':False,'natural_reachability':'NOT_VALIDATED','static':summary,'build':b}
 args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
