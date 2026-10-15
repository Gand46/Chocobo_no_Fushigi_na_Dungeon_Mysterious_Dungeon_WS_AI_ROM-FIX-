"""Run paired before/after synthetic native screenshots, one Mesen profile at a time."""
from pathlib import Path
import argparse,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--mesen',type=Path,required=True);a=p.parse_args()
rows=json.loads((ROOT/'build/qa26/layout_review.json').read_text())
env=os.environ.copy();env['LAYOUT_OBSERVER']=str(ROOT/'qa21/layout_observer.lua')
state=ROOT/'evidence/qa8_runs/q8_D1_boss_intro/checkpoint.mss';start=time.monotonic()
for prefix,rom in [('baseline',ROOT/'build/Chocobo_EN_v1.1_HF19_TEST.ws'),('candidate',ROOT/'build/qa26/candidate.ws')]:
    for row in rows:
        slug=row['id'].replace(':','_');out=ROOT/'evidence/qa26_runs'/(prefix+'_'+slug)
        subprocess.run([sys.executable,str(ROOT/'qa21/run.py'),str(rom),str(state),str(ROOT/'qa26/plans'/(slug+'.lua')),str(out),'--mesen',str(a.mesen.resolve()),'--timeout','15'],cwd=ROOT,env=env,check=True,stdout=subprocess.DEVNULL)
        meta=json.loads((out/'run.json').read_text());done=(out/'target_completed.txt').read_text().strip()=='true'if(out/'target_completed.txt').exists()else False
        print(json.dumps({'run':out.name,'exit':meta['exit'],'completed':meta['completed'],'target':done,'seconds':round(time.monotonic()-start,1)}),flush=True)
        if not(meta['exit']==0 and meta['completed']and done):raise SystemExit('Failed native session '+out.name)
