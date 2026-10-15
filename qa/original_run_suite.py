from pathlib import Path
import os,sys,time,subprocess,json,hashlib,signal
root=Path(__file__).resolve().parents[1]
rom,state,cases,out=map(lambda s:Path(s).resolve(),sys.argv[1:5]);out.mkdir(parents=True,exist_ok=True)
assert not (out/'completed.txt').exists()
mesen=root/'emulator/Mesen';script=Path(os.environ.get('SUITE_SCRIPT',str(root/'tools/native_suite.lua'))).resolve()
env=os.environ.copy();env.update(SUITE_OUT=str(out),SUITE_STATE=str(state),SUITE_CASES=str(cases),LD_PRELOAD=subprocess.check_output(['g++','-print-file-name=libstdc++.so.6'],text=True).strip())
cmd=[str(mesen),'--testRunner','--timeout=240','--enableStdout','--doNotSaveSettings','--debug.scriptWindow.allowIoOsAccess=true',str(script),str(rom)]
(out/'observer.lua').write_bytes(script.read_bytes())
t=time.monotonic()
with (out/'mesen.log').open('wb') as f:
 p=subprocess.Popen(cmd,env=env,cwd=mesen.parent,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
 try:code=p.wait(245)
 except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);code=p.wait()
meta={'method':'SYNTHETIC_BAG_FIXTURE_NATIVE_MENU','rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'state_sha256':hashlib.sha256(state.read_bytes()).hexdigest(),'cases_sha256':hashlib.sha256(cases.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'elapsed':time.monotonic()-t,'exit':code,'completed':(out/'completed.txt').exists(),'command':cmd}
(out/'run.json').write_text(json.dumps(meta,indent=2));(out/'cases.lua').write_bytes(cases.read_bytes());print(meta)
