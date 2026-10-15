from pathlib import Path
import argparse, subprocess, os, json, hashlib,time,signal,shutil
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('state');p.add_argument('plan',type=Path);p.add_argument('out',type=Path);p.add_argument('--timeout',type=int,default=45);p.add_argument('--mesen',type=Path,required=True);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
env=os.environ.copy();env.update(QA_OUT=str(a.out.resolve()),QA_STATE=str(Path(a.state).resolve()) if a.state!='-' else '',QA_PLAN=str(a.plan.resolve()))
lib=subprocess.check_output(['g++','-print-file-name=libstdc++.so.6'],text=True).strip();env['LD_PRELOAD']=lib
script=Path(__file__).with_name('driver.lua').resolve();cmd=[str(a.mesen.resolve()),'--testRunner',f'--timeout={a.timeout}','--enableStdout','--doNotSaveSettings','--debug.scriptWindow.allowIoOsAccess=true',str(script),str(a.rom.resolve())]
t=time.monotonic()
with (a.out/'mesen.log').open('w') as log:
 proc=subprocess.Popen(cmd,cwd=a.mesen.parent.resolve(),env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 try:code=proc.wait(a.timeout+3)
 except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);code=proc.wait()
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
r=dict(fixture_env={k:env[k] for k in ('ITEM_ID','ADD_DRINK') if k in env},exit=code,elapsed=time.monotonic()-t,command=cmd,rom_sha256=sha(a.rom),state_sha256=sha(Path(a.state)) if a.state!='-' else None,plan_sha256=sha(a.plan),script_sha256=sha(script),mesen_sha256=sha(a.mesen),completed=(a.out/'completed.txt').exists())
(a.out/'run.json').write_text(json.dumps(r,indent=2));shutil.copy(a.plan,a.out/'plan.lua');print(json.dumps(r))

raise SystemExit(0 if code == 0 and r["completed"] else 1)
