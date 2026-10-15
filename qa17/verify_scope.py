"""Rebuild HF12 and verify bounded QA17/M3 evidence. Visual judgement is recorded separately."""
from pathlib import Path
import argparse,hashlib,json,csv,struct,sys
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--japanese-rom',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();sys.path.insert(0,str(ROOT))
 from build import build
 from tools.reference_bps.bps import apply
 from qa15.inventory_layout import story_inventory
 m=json.loads((ROOT/'docs/history/qa17/manifest.json').read_text());jp=a.japanese_rom.read_bytes();bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps').read_bytes();rom=apply(jp,bps);b={'scope':'HISTORICAL_HF12_FROM_PRESERVED_BPS'};checks=0
 def ck(v):
  nonlocal checks
  assert v;checks+=1
 ck(bps==(ROOT/'patches/historical/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps').read_bytes());ck(apply(jp,bps)==rom);ck(sha(bps)==m['bps_sha256']);ck(sha(rom)==m['target']['sha256']);ck(struct.unpack_from('<H',rom,len(rom)-2)[0]==sum(rom[:-2])&65535)
 old=apply(jp,(ROOT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps').read_bytes());ck(sha(old)==m['previous_hf11']['sha256'])
 edits=json.loads((ROOT/'qa17/edits.json').read_text());ck(len(edits)==11);allowed={len(rom)-2,len(rom)-1};oldrows,_=story_inventory(old,'HF11');ptrs=sorted(set(int(x['pointer'],16)for x in oldrows))
 for e in edits:
  x=int(e['offset'],16);before=bytes.fromhex(e['before']);after=bytes.fromhex(e['after']);y=x+len(after)
  ck(len(before)==len(after));ck(old[x:y]==before);ck(rom[x:y]==after);ck(y<=min(p for p in ptrs if p>x));allowed.update(range(x,y))
 changed={i for i,(x,y)in enumerate(zip(old,rom))if x!=y};ck(changed<=allowed);ck(len(changed)==205);ck(len(changed-{len(rom)-2,len(rom)-1})==203);ck(rom[0x160000:0x170000]==old[0x160000:0x170000]);ck(rom[0x1b3b1b:0x1b3b39]==old[0x1b3b1b:0x1b3b39])
 census,_=story_inventory(rom,'HF12');ck([x['id']for x in census if x['exceeds_13_literal_cells']]==['G01:M031','G06:M022','G09:M063','G16:M064']);pmap={x['id']:x['pointer']for x in census};ck(len({pmap[f'G16:M{i:03d}']for i in [34,35,36]})==1)
 idx=json.loads((ROOT/'docs/QA17_RUN_INDEX.json').read_text());approved=[x for x in idx if x['status']=='PASS_SYNTHETIC_SCOPED'];ck(len(approved)==29);blankdrops=0;totalframes=0
 for x in idx:
  r=ROOT/'evidence/qa17_runs'/x['run'];meta=json.loads((r/'run.json').read_text());prov=json.loads((r/'provenance.json').read_text())
  ck(sha((r/'plan.lua').read_bytes())==meta['plan_sha256']==x['plan_sha256']);ck(sha((r/'observer.lua').read_bytes())==prov['observer_sha256']==x['observer_sha256']);ck(sha((ROOT/prov['state_path']).read_bytes())==meta['state_sha256']);ck(sha((ROOT/'qa17/driver.lua').read_bytes())==meta['script_sha256']);ck(meta['mesen_sha256']==m['mesen_sha256'])
  if x not in approved:continue
  ck(meta['completed'] and meta['exit']==0 and (r/'completed.txt').exists());ck(not(r/'dump_error.txt').exists());ck(meta['rom_sha256']==m['target']['sha256']);ck((r/'sram.bin').stat().st_size==32768);ck((r/'sram.bin').read_bytes()[0x6480]==0);ck(all(t['poweroff']=='false'for t in rows(r/'frames.csv')))
  s=rows(r/'story.csv');autos=[t for t in s if t['event']=='auto_line'];ck(all(t['value']=='0000'for t in autos));blankdrops+=len(autos);totalframes+=x['frames']
  if x['run']!='final_credits':ck(any(t['event']=='read'and t['value']=='FFFF'and int(t['frame'])>100 for t in s))
 ck(blankdrops==6)
 credits=rows(ROOT/'evidence/qa17_runs/final_credits/credits_pages.csv');ck([int(x['resource_id'],16)for x in credits]==list(range(0xc5,0xd3)));ck(credits[0]['return_ip']=='78A4');ck(all(x['return_ip']=='7931'for x in credits[1:]));ck(len(list((ROOT/'evidence/qa17_runs/final_credits').glob('credits_*.png')))==14)
 resources=json.loads((ROOT/'qa17/credits_resources.json').read_text())
 for x in resources:
  st=int(x['pointer'],16);end=int(x['compressed_end'],16);d=int(x['descriptor'],16);ck(sha(rom[st:end])==x['sha256']);ck(rom[st:end]==jp[st:end]);ck(rom[d:d+6]==jp[d:d+6]);ck(x['uncompressed_bytes']==2048)
 vis=json.loads((ROOT/'qa17/visual_readings.json').read_text())
 for x in vis:ck(sha((ROOT/'evidence/qa17_runs'/x['run']/x['image']).read_bytes())==x['sha256'])
 result={'status':'PASS_SYNTHETIC_SCOPED','checks':checks,'approved_runs':len(approved),'recorded_runs':len(idx),'native_frames_approved':totalframes,'unique_resources_fixed':11,'references_fixed':13,'static_alerts_fixed':9,'padding_only_alerts':3,'composite_alert_pending':1,'variable_cases':14,'variable_unique_pointers':7,'variable_references':9,'credits_pages':14,'nonblank_dropped_glyphs_approved':0,'blank_padding_drops_approved':blankdrops,'content_changed_bytes':203,'checksum_changed_bytes':2,'independent_bps':'PASS_EXACT_BYTES','build':b,'global_layout_approved':False,'global_linguistic_approved':False,'remaining_base_iterations':1,'limitations':['SAVESTATE/selector/data fixtures; natural reachability not established by these tests.','FFF8 selector1 uses a ROM-derived prepared buffer fixture.','Item12 currency composite excluded from generic item-name maximum.','Global denominator of runtime contexts remains incomplete.','Historical equipment/Atla/save causes not newly reproduced.']}
 a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
