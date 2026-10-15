"""Verify archived QA16 evidence and exact HF11 cumulative build. Visual approval is a separate human/model reading, not inferred here."""
import argparse,csv,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def main():
 p=argparse.ArgumentParser();p.add_argument('--japanese-rom',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args()
 sys.path.insert(0,str(ROOT));from build import build
 from tools.reference_bps.bps import apply as independent_apply
 manifest=json.loads((ROOT/'docs/history/qa16/manifest.json').read_text());src=a.japanese_rom.read_bytes();bps=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps').read_bytes();rom=independent_apply(src,bps);b={'scope':'HISTORICAL_HF11_FROM_PRESERVED_BPS'}
 assert hashlib.sha256(rom).hexdigest()==manifest['target']['sha256']
 assert bps==(ROOT/'patches/historical/Chocobo_EN_v1.1_HF11_TEST_JP_CCAA4853.bps').read_bytes()
 assert independent_apply(src,bps)==rom
 assert manifest['rom_changes_in_QA16']==0
 index=json.loads((ROOT/'docs/QA16_RUN_INDEX.json').read_text());approved=[x for x in index if x['status']=='PASS_SYNTHETIC_SCOPED'];assert len(approved)==16
 checkcount=0
 def check(ok):
  nonlocal checkcount
  assert ok;checkcount+=1
 window={int(x['id']):int(x['inner_width_px']) for x in rows(ROOT/'qa15/census_final/window_presets.csv')}
 guarded=0;store_events=0
 for x in index:
  d=ROOT/'evidence/qa16_runs'/x['run'];r=json.loads((d/'run.json').read_text());q=json.loads((d/'provenance.json').read_text())
  check(sha(d/'plan.lua')==r['plan_sha256']==x['plan_sha256']);check(sha(d/'observer.lua')==q['observer_sha256']==x['observer_sha256']);check(sha(ROOT/q['state_path'])==r['state_sha256']);check(sha(ROOT/'qa16/driver.lua')==r['script_sha256']);check(r['rom_sha256']==manifest['target']['sha256']);check(r['mesen_sha256']==manifest['mesen_sha256'])
  if x not in approved:continue
  check(r['exit']==0 and r['completed'] and (d/'completed.txt').exists());check(not(d/'dump_error.txt').exists());check((d/'sram.bin').stat().st_size==32768);check(all(z['poweroff']=='false' for z in rows(d/'frames.csv')))
  if(d/'stores.csv').exists():
   zz=rows(d/'stores.csv');guarded+=1;store_events+=len(zz)
   check(all(z['row_overflow']=='false' for z in zz));check(all((int(z['relative_byte'])+int(z['stride_bytes']))*4<=window[int(z['window'])] for z in zz))
 def mem(n):return(ROOT/'evidence/qa16_runs'/n/'sram.bin').read_bytes()
 def money(n):return int.from_bytes(mem(n)[0x72fd:0x7301],'little')
 def bag(n):
  r=mem(n);return [tuple(r[a:a+5])for a in range(0x6c9f,0x6c9f+r[0x6c9e]*5,5)if r[a]]
 check(money('shop_buy_purchase')==99999899);check(any(x[:2]==(1,73)for x in bag('shop_buy_purchase')))
 check(money('shop_buy_insufficient')==0);check(sorted(bag('shop_buy_insufficient'))==sorted([(1,136,99,0,16),(99,233,0,0,16),(1,157,157,0,16)]))
 check(money('shop_sell_confirm_plus')==2898);check(not any(x[1]==136 for x in bag('shop_sell_confirm_plus')));check(any(x[1]==157 for x in bag('shop_sell_confirm_plus')))
 check(money('shop_sell_confirm_minus')==1);check(not any(x[1]==157 for x in bag('shop_sell_confirm_minus')));check(any(x[1]==136 for x in bag('shop_sell_confirm_minus')))
 check(money('shop_sell_plus')==0);check(len(bag('shop_sell_plus'))==3)
 for n,expected in [('status_equipped_plus',{(26,3,136)}),('status_equipped_minus',{(26,3,136)}),('unknown_names_long',{(4,14,87),(4,14,93)}),('shop_buy_list',{(12,5,18),(12,5,19),(13,3,73),(13,3,89)}),('shop_sell_confirm_plus',{(15,3,136),(16,5,29),(16,5,30)}),('shop_sell_confirm_minus',{(15,3,157)})]:
  got={tuple(int(z[k])for k in ['window','family','index'])for z in rows(ROOT/'evidence/qa16_runs'/n/'getters.csv')};check(expected<=got)
 for x in json.loads((ROOT/'qa16/visual_readings.json').read_text()):check(sha(ROOT/'evidence/qa16_runs'/x['run']/x['image'])==x['sha256'])
 candidate=rows(ROOT/'evidence/qa16_runs/storage_tail/stores.csv');check(sum((int(z['relative_byte'])+int(z['stride_bytes']))*4>window[int(z['window'])]for z in candidate)==5)
 check(rom[0x1860af:0x1860cb]==src[0x1860af:0x1860cb]);check(rom[0x188f2c:0x188f64]==src[0x188f2c:0x188f64])
 # Do not bless timeout or incompatible render probes as gameplay defects.
 check(next(x for x in index if x['run']=='shop_default')['status']=='DIAGNOSTIC_EXCLUDED')
 result={'status':'PASS_SCOPED_EVIDENCE_BUILD_AND_TRANSACTION_CHECKS','checks':checkcount,'approved_synthetic_runs':len(approved),'recorded_runs':len(index),'approved_runs_with_store_monitor':guarded,'distinct_common_store_events_in_those_runs':store_events,'common_store_window_crossings_in_approved_runs':0,'candidate_forced_storage_crossings':5,'rom_changes':0,'target_sha256':hashlib.sha256(rom).hexdigest(),'bps_sha256':hashlib.sha256(bps).hexdigest(),'independent_bps':'PASS_EXACT_BYTES','build':b,'visual_review':'SEPARATE_RECORDED_IN_qa16/visual_readings.json','global_layout_approved':False,'global_linguistic_approved':False}
 a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
