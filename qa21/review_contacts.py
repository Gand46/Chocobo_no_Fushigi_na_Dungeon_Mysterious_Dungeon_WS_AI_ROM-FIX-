from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys
Q=Path('qa21');prefix=sys.argv[1] if len(sys.argv)>1 else 'final_';tr=json.loads((Q/'translations.json').read_text());items=[]
for id in sorted(tr):
 r=Q/'runs'/(prefix+id.replace(':','_'))
 if not(r/'run.json').exists():continue
 seen=set()
 for p in sorted(r.glob('page_*.png'))+list(r.glob('end_text.png')):
  px=hashlib.sha256(Image.open(p).convert('RGB').tobytes()).hexdigest()
  if px in seen:continue
  seen.add(px);items.append({'id':id,'path':str(p),'pixel_sha256':px})
for start in range(0,len(items),24):
 ch=items[start:start+24];im=Image.new('RGB',(896,164*((len(ch)+3)//4)),'#ddd');dr=ImageDraw.Draw(im)
 for i,x in enumerate(ch):
  xx=i%4*224;yy=i//4*164;dr.text((xx,yy),x['id']+' '+Path(x['path']).stem,fill='black');im.paste(Image.open(x['path']).crop((0,0,224,144)),(xx,yy+20))
 im.save(Q/f'{prefix}review_{start//24:02}.png')
(Q/f'{prefix}review_index.json').write_text(json.dumps(items,indent=2));print(len(items))
