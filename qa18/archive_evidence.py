from pathlib import Path
import json,shutil,hashlib,re
R=Path('delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014');Q=Path('qa18');O=R/'qa18';O.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();idx=[]
for p in Q.iterdir():
 if p.is_file() and p.suffix!='.bin':shutil.copy2(p,O/p.name)
for n in ['plans','census_final']:shutil.copytree(Q/n,O/n,dirs_exist_ok=True)
for r in sorted((Q/'runs').iterdir()):
 if not(r/'run.json').exists():continue
 m=json.loads((r/'run.json').read_text());out=R/'evidence/qa18_runs'/r.name;shutil.copytree(r,out,dirs_exist_ok=True);shutil.copy2(Q/'layout_observer.lua',out/'observer.lua')
 state='evidence/qa16_runs/shop_enter/checkpoint.mss' if ('slot'in r.name or 'storage'in r.name)else'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss'
 assert m['state_sha256']==sha(R/state)
 access=['SAVESTATE','SCRIPT_POINTER_INJECTION'if 'slot'in r.name or 'storage'in r.name else'MESSAGE_SELECTOR_INJECTION']
 if 'dyn_'in r.name:access.append('DATA_INJECTION')
 p={'state_path':state,'state_sha256':sha(R/state),'observer_sha256':sha(Q/'layout_observer.lua'),'access':access,'scope':'Native renderer. Synthetic entry does not demonstrate natural scene reachability, transaction completion or save persistence.'};(out/'provenance.json').write_text(json.dumps(p,indent=2)+'\n')
 frames=int((r/'completed.txt').read_text().split('=')[1]);idx.append({'run':r.name,'status':'PASS_SYNTHETIC_SCOPED'if r.name.startswith('final_')else'DIAGNOSTIC_EXCLUDED','rom_sha256':m['rom_sha256'],'plan_sha256':m['plan_sha256'],'observer_sha256':p['observer_sha256'],'frames':frames,'access':access})
(R/'docs/QA18_RUN_INDEX.json').write_text(json.dumps(idx,indent=2)+'\n');shutil.copy2(Q/'private/hf13_release/build_result.json',O/'build_result.json');print('runs',len(idx),'approved',sum(x['status']=='PASS_SYNTHETIC_SCOPED'for x in idx))
