from pathlib import Path
import subprocess,os,json,argparse,time,hashlib
p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--ids',default='qa21/audit_ids.json');a=p.parse_args();ids=json.loads(Path(a.ids).read_text());env=os.environ.copy();env['LAYOUT_OBSERVER']=str(Path('qa21/layout_observer.lua').resolve());state='work/Chocobo_QA20_V2/evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss'
for i,id in enumerate(ids):
 name=id.replace(':','_');out=Path('qa21/runs')/(a.prefix+name)
 if out.exists():
  meta=json.loads((out/'run.json').read_text())
  assert meta['completed'] and meta['rom_sha256']==hashlib.sha256(Path(a.rom).read_bytes()).hexdigest(),str(out)+' is not a completed run of this ROM'
  continue
 proc=subprocess.run(['python3','qa21/run.py',a.rom,state,'qa21/plans/'+name+'.lua',str(out),'--mesen','/tmp/chocobo_qa14_emulator/Mesen','--timeout','15'],env=env,capture_output=True,text=True)
 meta=json.loads((out/'run.json').read_text());print(f'{i+1}/{len(ids)} {id} exit={meta["exit"]} completed={meta["completed"]} target={(out/"target_completed.txt").read_text()if(out/"target_completed.txt").exists()else"missing"}',flush=True)
