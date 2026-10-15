"""Check paired native traces and arrange all pages for direct visual review."""
from pathlib import Path
import csv,hashlib,json,math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];Q=ROOT/'qa26';E=ROOT/'evidence/qa26_runs'
rows=json.loads((ROOT/'build/qa26/layout_review.json').read_text());pairs=[];runs=[]
hashes={'baseline':hashlib.sha256((ROOT/'build/Chocobo_EN_v1.1_HF19_TEST.ws').read_bytes()).hexdigest(),'candidate':hashlib.sha256((ROOT/'build/qa26/candidate.ws').read_bytes()).hexdigest()}
for item in rows:
    slug=item['id'].replace(':','_');pages=[]
    for prefix in ('baseline','candidate'):
        folder=E/(prefix+'_'+slug);meta=json.loads((folder/'run.json').read_text())
        assert meta['exit']==0 and meta['completed']and meta['rom_sha256']==hashes[prefix]
        assert(folder/'target_completed.txt').read_text().strip()=='true'
        trace=list(csv.DictReader((folder/'story.csv').open()))
        discarded=[x for x in trace if x['event']=='auto_line'and x['value']!='0000']
        assert not discarded,(folder.name,discarded)
        assert any(x['event']=='read'and x['value']=='FFFF'for x in trace)
        imgs=sorted(folder.glob('page_*.png'))or[folder/'end_text.png'];pages.append(imgs)
        runs.append({'run':folder.name,'frames':int((folder/'completed.txt').read_text().split('=')[1]),'pages':len(imgs),'nonblank_dropped':0,'rom_sha256':meta['rom_sha256']})
    assert len(pages[0])==len(pages[1]),item['id']
    for n,(before,after)in enumerate(zip(*pages),1):
        pairs.append({'id':item['id'],'page':n,'before':str(before.relative_to(ROOT)),'after':str(after.relative_to(ROOT)),'before_sha256':hashlib.sha256(before.read_bytes()).hexdigest(),'after_sha256':hashlib.sha256(after.read_bytes()).hexdigest()})
for start in range(0,len(pairs),6):
    canvas=Image.new('RGB',(464,6*185),'#e8ede9');d=ImageDraw.Draw(canvas)
    for idx,pair in enumerate(pairs[start:start+6]):
        y=idx*185;d.text((4,y+2),f'{pair["id"]} / {pair["page"]}  HF19',fill='black');d.text((236,y+2),'HF20 candidate',fill='black')
        for side,key in enumerate(('before','after')):
            with Image.open(ROOT/pair[key])as im:canvas.paste(im.convert('RGB'),(side*232+4,y+18))
    canvas.save(Q/f'comparison_{start//6+1:02d}.png')
(Q/'native_pairs.json').write_text(json.dumps(pairs,indent=2)+'\n')
result={'status':'PASS_NATIVE_TRACE_NOT_YET_VISUAL','resources':len(rows),'sessions':len(runs),'paired_pages':len(pairs),'frames':sum(x['frames']for x in runs),'nonblank_dropped':0,'runs':runs}
(Q/'runtime_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='runs'}))
