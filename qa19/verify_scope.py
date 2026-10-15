"""Rebuild final HF14 and verify scoped runtime evidence; never equate exit 0 with PASS."""
from pathlib import Path
import json,hashlib,csv,struct,sys,argparse
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--japanese-rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(ROOT));from build import build
 from tools.reference_bps.bps import apply
 from qa15.inventory_layout import story_inventory,getter_inventory
 from qa18.scan_layout import scan
 sha=lambda b:hashlib.sha256(b).hexdigest();m=json.loads((ROOT/'docs/history/qa19/manifest.json').read_text());jp=a.japanese_rom.read_bytes();bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(jp,bps);b={'scope':'HISTORICAL_HF14'};old=apply(jp,(ROOT/'patches/historical/Chocobo_EN_v1.1_HF13_TEST_JP_CCAA4853.bps').read_bytes());checks=0
 def ck(v):
  nonlocal checks
  assert v;checks+=1
 ck(sha(old)==m['previous_hf13']['sha256']);ck(apply(jp,bps)==rom);ck(bps==(ROOT/'patches/historical/Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps').read_bytes());ck(sha(bps)==m['bps_sha256']);ck(sha(rom)==m['target']['sha256']);ck(sum(rom[:-2])&65535==struct.unpack('<H',rom[-2:])[0]);ck(len(rom)==len(old)==2097152)
 edits=json.loads((ROOT/'qa19/edits.json').read_text());allowed={len(rom)-2,len(rom)-1}
 for e in edits:
  x=int(e['offset'],16);before=bytes.fromhex(e['before']);after=bytes.fromhex(e['after']);y=x+len(after);ck(len(before)==len(after));ck(old[x:y]==before);ck(rom[x:y]==after);allowed.update(range(x,y))
 changed={i for i,(x,y)in enumerate(zip(old,rom))if x!=y};ck(changed<=allowed);ck(len(changed)==m['changed_bytes_vs_hf13']);ck(old[0x6e000:0x6ff00]==jp[0x6e000:0x6ff00]==b'\xff'*0x1f00);ck(rom[0x160000:0x170000]==old[0x160000:0x170000])
 st0,_=story_inventory(old,'HF13');st1,_=story_inventory(rom,'HF14');a0={x['id']:x for x in st0};a1={x['id']:x for x in st1};tr=json.loads((ROOT/'qa19/translations.json').read_text());ck(len(st0)==len(st1)==3488);ck(set(a0)==set(a1));ck({x for x in a0 if a0[x]['stream_sha256']!=a1[x]['stream_sha256']}==set(tr));ck({x for x in a0 if a0[x]['pointer']!=a1[x]['pointer']}==set(tr));ck(len(tr)==36)
 for id in tr:ck(a1[id]['terminated']);ck(a1[id]['max_literal_cells']<=13);ck(a0[id]['bank']==a1[id]['bank']==6)
 g0,_=getter_inventory(old,'HF13');g1,_=getter_inventory(rom,'HF14');ck([(x['id'],x['pointer'],x['stream_sha256'])for x in g0]==[(x['id'],x['pointer'],x['stream_sha256'])for x in g1]);_,_,_,summary=scan(rom);ck(summary['story_unterminated']==summary['getter_unterminated']==0);ck(summary['horizontal_candidates']==['G01:M031','G06:M022','G09:M063']);ck(summary['vertical_candidates']==[])
 ids=json.loads((ROOT/'qa19/audit_ids.json').read_text());frames=0;blank=0;native=[];getrows=lambda p:list(csv.DictReader(p.open()))
 for id in ids:
  r=ROOT/'evidence/qa19_runs'/('release2_'+id.replace(':','_'));meta=json.loads((r/'run.json').read_text());ck(meta['completed']and meta['exit']==0);ck((r/'target_completed.txt').read_text()=='true');ck(meta['rom_sha256']==m['target']['sha256']);ck(meta['script_sha256']==sha((ROOT/'qa19/driver.lua').read_bytes()));ck(meta['plan_sha256']==sha((r/'plan.lua').read_bytes()));ck(meta['state_sha256']==sha((ROOT/'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss').read_bytes()));ck(not(r/'dump_error.txt').exists());ck((r/'sram.bin').stat().st_size==32768);ck(all(x['poweroff']=='false'for x in getrows(r/'frames.csv')))
  group=int(id[1:3]);msg=int(id[5:]);story=[x for x in getrows(r/'story.csv')if int(x['group'])==group and int(x['message'])==msg];ck(any(x['event']=='read'and x['value']=='FFFF'and not(int(x['state'],16)&0x40)for x in story));auto=[x for x in story if x['event']=='auto_line'];ck(all(x['value']=='0000'for x in auto));blank+=len(auto);frames+=int((r/'completed.txt').read_text().split('=')[1]);native.append(id)
 # Actual one-line Slot Point consumer, entered synthetically through its script.
 r=ROOT/'evidence/qa19_runs/release2_slot_native';meta=json.loads((r/'run.json').read_text());ck(meta['rom_sha256']==m['target']['sha256']);ck(meta['exit']==0 and meta['completed']);ck((r/'injection.txt').read_text()=='true');events=getrows(r/'script.csv');ck(any(x['bank']=='E0'and x['pointer']=='59BF'and x['opcode']=='28'for x in events));ck(any(x['bank']=='E0'and x['pointer']=='59C2'and x['opcode']=='7B'for x in events));story=[x for x in getrows(r/'story.csv')if x['group']=='16'and x['message']=='64'];ck({x['line_limit']for x in story}=={'1'});ck(sum(x['value']=='FFF2'and x['event']=='read'for x in story)>=3);ck(all(x['value']=='0000'for x in story if x['event']=='auto_line'));frames+=int((r/'completed.txt').read_text().split('=')[1])
 vis=json.loads((ROOT/'qa19/visual_readings.json').read_text())
 for x in vis:ck(sha((ROOT/'evidence/qa19_runs'/x['run']/x['image']).read_bytes())==x['sha256'])
 review=json.loads((ROOT/'qa19/linguistic_review.json').read_text());ck(len(review)==83);ck(sum(x['linguistic_status']=='PASS_REVIEWED_SCOPED'for x in review)==82)
 result={'status':'PASS_SYNTHETIC_SCOPED_WITH_CONTEXT_PENDING','validation':'V1_OF_5_EXECUTED','checks':checks,'references_audited':83,'references_corrected':36,'linguistic_scoped_pass':82,'context_pending':['G16:M073 host phrase'],'native_sessions_passed':84,'native_frames':frames,'visual_readings':len(vis),'nonblank_dropped_glyphs':0,'blank_padding_drops':blank,'changed_bytes_vs_hf13':len(changed),'independent_bps':'PASS_EXACT_BYTES','global_visual_approved':False,'global_linguistic_approved':False,'actual_menu_consumers':'V2_PENDING; Slot one-line consumer covered','natural_reachability':'NOT_VALIDATED','static':summary,'build':b};a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
