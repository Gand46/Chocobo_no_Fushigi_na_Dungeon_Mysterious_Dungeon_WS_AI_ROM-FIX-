from pathlib import Path
import os,subprocess,json,shutil
base=Path('delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014');env=os.environ.copy();env['LAYOUT_OBSERVER']=str(Path('qa18/layout_observer.lua').resolve());cases=[]
for p in sorted(Path('qa18/plans').glob('G*.lua')):cases.append((p,'final_'+p.stem,base/'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss'))
cases.append((Path('qa18/plans/slot_native.lua'),'final_slot_native',base/'evidence/qa16_runs/shop_enter/checkpoint.mss'))
for n in ['dyn_G00_M253_max','dyn_G16_M034_max']:
 p=Path('qa18/plans')/(n+'.lua');shutil.copy2(Path('qa17/plans')/p.name,p);cases.append((p,'final_'+n,base/'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss'))
for p,name,state in cases:
 a=subprocess.run(['python3','qa18/run.py','qa18/private/hf13_release/Chocobo_EN_v1.1_HF13_TEST.ws',str(state),str(p),'qa18/runs/'+name,'--mesen','/tmp/chocobo_qa14_emulator/Mesen','--timeout','15'],env=env,capture_output=True,text=True);print(name,a.stdout.strip(),flush=True)
