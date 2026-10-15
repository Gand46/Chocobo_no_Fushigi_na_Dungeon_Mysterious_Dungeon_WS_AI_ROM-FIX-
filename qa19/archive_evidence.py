from pathlib import Path
import json,shutil,hashlib
R=Path('delivery/Chocobo_EN_v1.1_HF14_TEST_Fuentes_QA19_V1_20261014');Q=Path('qa19');O=R/'qa19';O.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();idx=[]
for p in Q.iterdir():
 if p.is_file()and p.suffix in ['.py','.lua','.json','.png','.txt']:shutil.copy2(p,O/p.name)
shutil.copytree(Q/'plans',O/'plans',dirs_exist_ok=True)
for r in sorted((Q/'runs').iterdir()):
 if not(r/'run.json').exists():continue
 m=json.loads((r/'run.json').read_text());approved=r.name.startswith('release2_');out=R/'evidence/qa19_runs'/r.name;out.mkdir(parents=True,exist_ok=True)
 if approved:shutil.copytree(r,out,dirs_exist_ok=True)
 else:
  for p in r.iterdir():
   if p.is_file()and(p.suffix in ['.json','.log','.lua','.txt','.png']):shutil.copy2(p,out/p.name)
 shutil.copy2(Q/'layout_observer.lua',out/'observer.lua');state='evidence/qa16_runs/shop_enter/checkpoint.mss'if'slot_native'in r.name else'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss'
 pr={'state_path':state,'state_sha256':sha(R/state),'observer_sha256':sha(Q/'layout_observer.lua'),'access':['SAVESTATE','SCRIPT_POINTER_INJECTION'if'slot_native'in r.name else'MESSAGE_SELECTOR_INJECTION'],'scope':'Synthetic native rendering; no natural reachability claim. Long item name and 65535 injected for dynamic refs. Diagnostic candidate_ hash may reflect a changed on-disk candidate; excluded from all release proofs.'};(out/'provenance.json').write_text(json.dumps(pr,indent=2)+'\n')
 idx.append({'run':r.name,'status':'PASS_SYNTHETIC_SCOPED'if approved else'DIAGNOSTIC_EXCLUDED','rom_sha256':m['rom_sha256'],'frames':int((r/'completed.txt').read_text().split('=')[1])if(r/'completed.txt').exists()else None,'target_completed':(r/'target_completed.txt').read_text()if(r/'target_completed.txt').exists()else None,'diagnostic_retention':'logs, plans, screenshots; final release additionally retains memory dumps/CDL/checkpoint'})
(R/'docs/QA19_RUN_INDEX.json').write_text(json.dumps(idx,indent=2)+'\n');shutil.copy2(Q/'private/hf14_release/build_result.json',O/'build_result.json');print('approved',sum(x['status']=='PASS_SYNTHETIC_SCOPED'for x in idx),'all',len(idx))
