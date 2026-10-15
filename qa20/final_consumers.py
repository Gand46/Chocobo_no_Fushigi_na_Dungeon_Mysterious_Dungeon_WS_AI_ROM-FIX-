from pathlib import Path
import subprocess,os
root=Path('work/Chocobo_QA20_V2');env=os.environ.copy();env['LAYOUT_OBSERVER']=str(Path('qa20/layout_observer.lua').resolve())
for name,st,save in [('menu_empty','-','qa20/private/empty.sav'),('menu_saved','-',str(root/'evidence/qa13_runs/q13_equipment_native_save/native_save_after.sav')),('save_native',str(root/'evidence/qa13_runs/q13_equipment_checkpoint/checkpoint.mss'),None)]:
 cmd=['python3','qa20/run.py','qa20/private/candidate.ws',st,'qa20/plans/'+name+'.lua','qa20/runs/release_'+name,'--mesen','/tmp/chocobo_qa14_emulator/Mesen','--timeout','20']
 if save:cmd+=['--input-save',save]
 if st!='-':assert Path(st).exists(),st
 subprocess.run(cmd,env=env,check=True)
