from pathlib import Path
from PIL import Image,ImageDraw
import json
Q=Path('qa21');items=[]
for name in ['quantity_unknown','unknown_names_long','status_equipped_plus','status_equipped_minus']:
 for f in [420,600,720,840,960,1080,1200,1800]:
  for lang in ['JP','HF16V3']:
   p=Q/'runs'/f'ui_{lang}_{name}'/f'f{f:05}.png'
   if p.exists():items.append({'path':str(p.relative_to(Q/'runs')),'caption':lang+' '+name+' '+str(f)})
for p in sorted((Q/'runs/fused_HF16V3').glob('*.png')):
 for lang in ['JP','HF16V3']:items.append({'path':f'fused_{lang}/'+p.name,'caption':lang+' '+p.stem})
for start in range(0,len(items),24):
 ch=items[start:start+24];im=Image.new('RGB',(896,168*((len(ch)+3)//4)),'#ddd');dr=ImageDraw.Draw(im)
 for k,x in enumerate(ch):
  xx=k%4*224;yy=k//4*168;dr.text((xx,yy),x['caption'],fill='black');im.paste(Image.open(Q/'runs'/x['path']).crop((0,0,224,144)),(xx,yy+24))
 im.save(Q/f'supplemental_contact_{start//24:02}.png')
(Q/'supplemental_readings_index.json').write_text(json.dumps(items,indent=2));print(len(items))
