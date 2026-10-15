#!/usr/bin/env python3
"""Run a bounded Mesen audit (input-only by default; optional synthetic mode) and record exact inputs and environment."""
from pathlib import Path
import os,subprocess,sys,hashlib,json,time,signal,shutil,argparse
p=argparse.ArgumentParser();p.add_argument('rom');p.add_argument('route');p.add_argument('out');p.add_argument('--frames',type=int,default=2400);p.add_argument('--timeout',type=int,default=35);p.add_argument('--mesen',default=str(Path(__file__).parent/'Mesen'));p.add_argument('--clean',action='store_true');p.add_argument('--resume');args=p.parse_args()
if args.frames <= 0 or args.timeout <= 0: p.error('Frames and timeout must be positive')
rom=Path(args.rom).resolve();route=Path(args.route).resolve();out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
if (out/'completed.txt').exists(): p.error('Use a new output directory to preserve prior evidence')
mesen=Path(args.mesen).resolve()
if args.clean:
 for name in ['Saves','Debugger']:
  for f in (mesen.parent/name).glob(rom.stem+'.*'):f.unlink()
env=os.environ.copy();env['LD_PRELOAD']=subprocess.check_output(['g++','-print-file-name=libstdc++.so.6'],text=True).strip();env.update(AUDIT_OUT=str(out),AUDIT_ROUTE=str(route),AUDIT_FRAMES=str(args.frames))
env.pop('AUDIT_RESUME',None)
if args.resume:env['AUDIT_RESUME']=str(Path(args.resume).resolve())
synthetic=env.get('AUDIT_SYNTHETIC_TARGET')
shutil.copyfile(Path(__file__).parent/'runtime_audit.lua',out/'runtime_audit.lua')
cmd=[str(mesen),'--testRunner',f'--timeout={args.timeout}','--enableStdout','--doNotSaveSettings','--debug.scriptWindow.allowIoOsAccess=true',str(Path(__file__).parent/'runtime_audit.lua'),str(rom)]
t=time.monotonic();timedout=False
proc=subprocess.Popen(cmd,cwd=mesen.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
try:log=proc.communicate(timeout=args.timeout+5)[0]
except subprocess.TimeoutExpired:
 timedout=True;os.killpg(proc.pid,signal.SIGKILL);log=proc.communicate()[0]
(out/'mesen.log').write_bytes(log);shutil.copyfile(route,out/'route.lua')
meta=dict(command=cmd,frames_requested=args.frames,timeout_seconds=args.timeout,elapsed_seconds=round(time.monotonic()-t,3),exit=proc.returncode,timed_out=timedout,completed=(out/'completed.txt').exists(),rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),route_sha256=hashlib.sha256(route.read_bytes()).hexdigest(),mesen_sha256=hashlib.sha256(mesen.read_bytes()).hexdigest(),method='SYNTHETIC_RESOURCE_SUBSTITUTION' if synthetic else ('SAVESTATE_CONTINUATION' if args.resume else 'SCRIPTED_NATURAL'),synthetic_target=synthetic,trace_text=env.get('AUDIT_TRACE_TEXT')=='1',observer_sha256=hashlib.sha256((out/'runtime_audit.lua').read_bytes()).hexdigest(),resume=args.resume,clean=args.clean)
(out/'run.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2));print(log.decode(errors='replace')[-2000:])
