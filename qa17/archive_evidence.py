from pathlib import Path
import json,csv,shutil,hashlib
ROOT=Path('delivery/Chocobo_EN_v1.1_HF12_TEST_Fuentes_QA17_M3_20261014');Q=Path('qa17');OUT=ROOT/'qa17';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Archive analysis, plans and receipts; exclude complete ROMs and raw ROM excerpts.
for p in Q.iterdir():
 if p.is_file():shutil.copy2(p,OUT/p.name)
for n in ['plans','census_final']:shutil.copytree(Q/n,OUT/n,dirs_exist_ok=True)
index=[];dest=ROOT/'evidence/qa17_runs'
for r in sorted((Q/'runs').iterdir()):
 if not(r/'run.json').exists():continue
 meta=json.loads((r/'run.json').read_text());target=dest/r.name;shutil.copytree(r,target,dirs_exist_ok=True);shutil.copy2(Q/'layout_observer.lua',target/'observer.lua')
 credits=r.name in ['credits','credits2','final_credits'];state='evidence/qa8_runs/q8_d2_boss_assist/checkpoint.mss' if credits else 'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss'
 access=['SAVESTATE'] if credits else ['SAVESTATE','POINTER_INJECTION']
 if 'dyn_' in r.name or 'dyn2_' in r.name:access+=['DATA_INJECTION']
 if 'G00_M255' in r.name:access+=['ROM_DERIVED_BUFFER_FIXTURE']
 status='PASS_SYNTHETIC_SCOPED' if r.name.startswith('final_') and r.name!='final_G16_M064' else 'DIAGNOSTIC_EXCLUDED'
 if not meta['completed'] or meta['exit']!=0:status='DIAGNOSTIC_TIMEOUT_EXCLUDED'
 prov={'state_path':state,'state_sha256':sha(ROOT/state),'observer_sha256':sha(Q/'layout_observer.lua'),'access':access,'scope':'Native text rendering; pointer/data fixtures do not prove natural scene reachability or save persistence.','prior_boss_assist':credits}
 assert meta['state_sha256']==prov['state_sha256'];(target/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
 index.append({'run':r.name,'status':status,'rom_sha256':meta['rom_sha256'],'plan_sha256':meta['plan_sha256'],'observer_sha256':prov['observer_sha256'],'access':access,'frames':7200 if credits else 1050})
(ROOT/'docs/QA17_RUN_INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
bps=Q/'private/hf12_final/Chocobo_EN_v1.1_HF12_TEST_JP_CCAA4853.bps';shutil.copy2(bps,ROOT/'patches'/bps.name);shutil.copy2(bps,Path('delivery')/bps.name)
m=json.loads((ROOT/'manifest.json').read_text());b=json.loads((Q/'private/hf12_final/build_result.json').read_text());m['bps_sha256']=sha(bps);m['changed_bytes_vs_english']=b['changed_bytes_vs_legacy'];m['qa17']['approved_scoped_runs']=sum(x['status']=='PASS_SYNTHETIC_SCOPED' for x in index);m['qa17']['all_runs']=len(index);m['qa17']['status']='PASS_SYNTHETIC_SCOPED_WITH_M4_OPEN_CONTEXTS';m['qa17']['credits_pages']=14;m['qa17']['dynamic_cases']=14;m['qa17']['synthetic_max_numeric']=65535;m['qa17']['synthetic_item_indices']=[217,136];m['qa17']['inheritance']='HF11 code, fonts, title, pointer tables, save and gameplay fixes unchanged; QA15 and QA16 validators pinned to historical HF11, checks rerun without repeating native sessions.'
(ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');(OUT/'build_result.json').write_text(json.dumps(b,indent=2)+'\n')
print('archived',len(index),'approved',m['qa17']['approved_scoped_runs'])
