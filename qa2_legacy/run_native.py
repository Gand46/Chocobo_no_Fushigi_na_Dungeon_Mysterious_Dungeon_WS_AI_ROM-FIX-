#!/usr/bin/env python3
"""Run an explicitly synthetic Mesen suite with fixed case and wall-clock limits.
Linux x86_64 was tested. A successful launcher exit does not confer visual approval.
"""
import argparse, hashlib, json, os, shutil, signal, subprocess, time
from pathlib import Path
HERE=Path(__file__).resolve().parent.parent/'qa'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('rom',type=Path);p.add_argument('state',type=Path);p.add_argument('out',type=Path)
p.add_argument('--mesen',required=True,type=Path)
p.add_argument('--suite',choices=['equipment','resources'],required=True)
p.add_argument('--cases',type=Path,required=True)
p.add_argument('--timeout',type=int,default=240)
a=p.parse_args()
if not 1<=a.timeout<=3600:p.error('Use a positive timeout of at most 3600 seconds')
for f in [a.rom,a.state,a.mesen]:
    if not f.is_file():p.error(f'Input not found: {f}')
if a.out.exists() and any(a.out.iterdir()):p.error('Choose an empty output folder')
a.out.mkdir(parents=True,exist_ok=True)
script=HERE/('native_suite.lua' if a.suite=='equipment' else 'resource_suite.lua')
cases=a.cases.resolve()
env=os.environ.copy();env.update(SUITE_OUT=str(a.out.resolve()),SUITE_STATE=str(a.state.resolve()),SUITE_CASES=str(cases))
if os.name=='posix' and shutil.which('g++'):
    lib=subprocess.check_output(['g++','-print-file-name=libstdc++.so.6'],text=True).strip()
    if Path(lib).is_file():env['LD_PRELOAD']=lib
cmd=[str(a.mesen.resolve()),'--testRunner',f'--timeout={a.timeout}','--enableStdout','--doNotSaveSettings','--debug.scriptWindow.allowIoOsAccess=true',str(script),str(a.rom.resolve())]
start=time.monotonic();timedout=False
with (a.out/'mesen.log').open('wb') as log:
    proc=subprocess.Popen(cmd,env=env,cwd=a.mesen.parent.resolve(),stdout=log,stderr=subprocess.STDOUT,start_new_session=(os.name=='posix'))
    try:code=proc.wait(a.timeout+5)
    except subprocess.TimeoutExpired:
        timedout=True
        if os.name=='posix':os.killpg(proc.pid,signal.SIGKILL)
        else:proc.kill()
        code=proc.wait()
meta={'method':'SYNTHETIC_SINGLE_BAG_RECORD_NATIVE_MENU' if a.suite=='equipment' else 'SYNTHETIC_RESOURCE_REPLAY_PLUS_SINGLE_BAG_RECORD','rom_sha256':hashlib.sha256(a.rom.read_bytes()).hexdigest(),'state_sha256':hashlib.sha256(a.state.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'cases_sha256':hashlib.sha256(cases.read_bytes()).hexdigest(),'command':cmd,'elapsed_seconds':time.monotonic()-start,'timed_out':timedout,'exit':code,'completed':(a.out/'completed.txt').is_file()}
(a.out/'run.json').write_text(json.dumps(meta,indent=2)+'\n')
shutil.copy(script,a.out/'observer.lua');shutil.copy(cases,a.out/'cases.lua')
print(json.dumps(meta,indent=2))
raise SystemExit(0 if code==0 and meta['completed'] and not timedout else 1)
