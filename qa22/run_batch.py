from pathlib import Path
import argparse,subprocess,os,json,hashlib,sys
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--prefix',required=True);p.add_argument('--ids',type=Path,default=Path('qa22/audit_ids.json'));p.add_argument('--timeout',type=int,default=15);a=p.parse_args()
ids=json.loads(a.ids.read_text());env=os.environ.copy();env['LAYOUT_OBSERVER']=str(Path('qa21/layout_observer.lua').resolve());state=Path('evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();target=sha(a.rom)
for i,id in enumerate(ids):
 name=id.replace(':','_');out=Path('evidence/qa22_runs')/(a.prefix+name)
 if out.exists():
  meta=json.loads((out/'run.json').read_text());assert meta['completed'] and meta['rom_sha256']==target and meta['state_sha256']==sha(state),str(out)
  continue
 proc=subprocess.run([sys.executable,'qa21/run.py',str(a.rom),str(state),str(Path('qa22/plans')/(name+'.lua')),str(out),'--mesen','/tmp/chocobo_qa14_emulator/Mesen','--timeout',str(a.timeout)],env=env,capture_output=True,text=True)
 if proc.returncode:print(f'{i+1}/{len(ids)} {id} LAUNCH_FAILED {proc.stderr}',flush=True);raise RuntimeError(id)
 meta=json.loads((out/'run.json').read_text());target_ok=(out/'target_completed.txt').read_text().strip() if (out/'target_completed.txt').exists() else'MISSING'
 print(f'{i+1}/{len(ids)} {id} exit={meta["exit"]} completed={meta["completed"]} target={target_ok}',flush=True)
 if not meta['completed'] or not target_ok=='true':raise RuntimeError(id+' incomplete')
