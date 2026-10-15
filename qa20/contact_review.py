from pathlib import Path
from PIL import Image,ImageDraw
import sys,json
prefix=sys.argv[1];items=[]
for id in json.loads(Path('qa20/audit_ids.json').read_text()):
 d=Path('qa20/runs')/(prefix+id.replace(':','_'))
 if not(d/'completed.txt').exists():continue
 ps=sorted(d.glob('page_*.png'))or list(d.glob('end_text.png'))
 for p in ps:items.append((id,p))
for start in range(0,len(items),24):
 chunk=items[start:start+24];im=Image.new('RGB',(896,((len(chunk)+3)//4)*164),'#ddd');dr=ImageDraw.Draw(im)
 for j,(id,p)in enumerate(chunk):
  x=j%4*224;y=j//4*164;dr.text((x,y),id+' '+p.stem,fill='black');im.paste(Image.open(p),(x,y+20))
 im.save(f'qa20/{prefix}review_{start//24:02}.png')
Path('qa20/'+prefix+'pages.json').write_text(json.dumps([{'id':id,'path':str(p)}for id,p in items],indent=2));print(len(items))
