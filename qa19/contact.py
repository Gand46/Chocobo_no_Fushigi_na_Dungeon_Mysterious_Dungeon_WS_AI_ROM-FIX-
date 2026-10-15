from PIL import Image,ImageDraw
from pathlib import Path
import sys
prefix=sys.argv[1] if len(sys.argv)>1 else 'final_'
imgs=[]
for r in sorted(Path('qa19/runs').glob(prefix+'*')):
 ps=sorted(r.glob('page_*.png'))+list(r.glob('end_text.png'))
 seen=set();ps=[p for p in ps if not(p.read_bytes()in seen or seen.add(p.read_bytes()))]
 for p in ps:imgs.append((r.name[len(prefix):]+':'+p.stem,p))
for start in range(0,len(imgs),24):
 chunk=imgs[start:start+24];o=Image.new('RGB',(896,((len(chunk)+3)//4)*164),'#ddd');d=ImageDraw.Draw(o)
 for k,(label,p) in enumerate(chunk):
  x=k%4*224;y=k//4*164;d.text((x,y),label,fill='black');o.paste(Image.open(p).convert('RGB'),(x,y+20))
 o.save(f'qa19/{prefix}contact_{start//24:02}.png')
print(len(imgs))
