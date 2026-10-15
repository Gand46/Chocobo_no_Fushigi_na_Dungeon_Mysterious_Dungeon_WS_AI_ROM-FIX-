from pathlib import Path
import time,subprocess,os
while not Path('qa20/runs/final_G04_M020/completed.txt').exists():time.sleep(1)
env=os.environ.copy();env['LAYOUT_OBSERVER']=str(Path('qa20/layout_observer.lua').resolve());root=Path('work/Chocobo_QA20_V2');state=str(root/'evidence/qa13_runs/q13_equipment_sorted/checkpoint.mss')
for name,st,save in [('menu_empty','-','qa20/private/empty.sav'),('menu_saved','-',str(root/'evidence/qa13_runs/q13_equipment_native_save/native_save_after.sav')),('save_native',state,None)]:
 cmd=['python3','qa20/run.py','qa20/private/candidate.ws',st,'qa20/plans/'+name+'.lua','qa20/runs/'+name,'--mesen','/tmp/chocobo_qa14_emulator/Mesen','--timeout','30']
 if save:cmd+=['--input-save',save]
 subprocess.run(cmd,env=env,check=True)
