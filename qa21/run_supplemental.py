from pathlib import Path
import subprocess,os,shutil,json,sys
Q=Path('qa21');R=Path('work/Chocobo_QA20_V2');state=R/'evidence/qa3/q3_dungeon/checkpoint.mss';env=os.environ.copy();env['LAYOUT_OBSERVER']=str((Q/'layout_observer.lua').resolve());names=['quantity_unknown','unknown_names_long','status_equipped_plus','status_equipped_minus'];(Q/'supplemental_plans').mkdir(exist_ok=True);suite=Q/'fused_suite';suite.mkdir(exist_ok=True)
for n in names:shutil.copy2(R/'qa16'/f'{n}.lua',Q/'supplemental_plans'/f'{n}.lua')
for a,b in [('observer.lua','native_suite.lua'),('cases.lua','cases_equip.lua')]:shutil.copy2(R/'evidence/qa12_runs/q12_fused_valid'/a,suite/b)
shutil.copy2(R/'qa12/item_layout/run_suite.py',suite/'run_suite.py')
for label,rom in [('JP',Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws')),('HF16V3',Q/'private/candidate.ws')]:
 if '--hf16-only' in sys.argv and label=='JP':continue
 for n in names:
  out=Q/'runs'/f'ui_{label}_{n}'
  subprocess.run(['python3',str(Q/'run.py'),str(rom),str(state),str(Q/'supplemental_plans'/f'{n}.lua'),str(out),'--mesen','/tmp/chocobo_qa14_emulator/Mesen','--timeout','20'],env=env,check=True,stdout=subprocess.DEVNULL)
  print(label,n,json.loads((out/'run.json').read_text())['completed'],flush=True)
 out=Q/'runs'/f'fused_{label}'
 subprocess.run(['python3',str(suite/'run_suite.py'),str(rom),str(state),str(out),'--mesen','/tmp/chocobo_qa14_emulator/Mesen','--suite','equipment','--timeout','30'],env=env,check=True,stdout=subprocess.DEVNULL)
 print(label,'fused',json.loads((out/'run.json').read_text())['completed'],flush=True)
