from pathlib import Path
from PIL import Image,ImageDraw
import sys
folder=Path(sys.argv[1]);prefix=sys.argv[2]
ps=sorted(folder.glob('*_f720.png'))
for g in range(0,len(ps),24):
 batch=ps[g:g+24];im=Image.new('RGB',(224*4,174*((len(batch)+3)//4)),'white');d=ImageDraw.Draw(im)
 for i,p in enumerate(batch):
  x=i%4*224;y=i//4*174;d.text((x+3,y+2),p.stem,fill='black');im.paste(Image.open(p),(x,y+17))
 im.save(f'{prefix}_{g//24:02d}.png')
print('screens',len(ps))
