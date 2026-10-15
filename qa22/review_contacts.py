from pathlib import Path
from PIL import Image,ImageDraw
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--prefix',required=True);p.add_argument('--changed-only',action='store_true');a=p.parse_args()
ids=list(json.loads(Path('qa22/translations.json').read_text())) if a.changed_only else json.loads(Path('qa22/audit_ids.json').read_text())
rows=[]
for id in ids:
 d=Path('evidence/qa22_runs')/(a.prefix+id.replace(':','_'))
 if not d.exists():continue
 seen=set()
 for f in sorted(d.glob('page_*.png'))+list(d.glob('end_text.png')):
  h=hashlib.sha256(Image.open(f).convert('RGB').tobytes()).hexdigest()
  if h in seen:continue
  seen.add(h);rows.append((id,f))
for start in range(0,len(rows),12):
 group=rows[start:start+12];out=Image.new('RGB',(896,164*((len(group)+3)//4)),'#e6e6e6');draw=ImageDraw.Draw(out)
 for n,(id,pic) in enumerate(group):
  x=n%4*224;y=n//4*164;draw.text((x,y),id+' '+pic.stem,fill='black');out.paste(Image.open(pic).convert('RGB').crop((0,0,224,144)),(x,y+20))
 out.save(f'qa22/{a.prefix}{"changed" if a.changed_only else "all"}_{start//12:02d}.png')
print('ids',len(ids),'distinct images',len(rows),'contacts',(len(rows)+11)//12)
