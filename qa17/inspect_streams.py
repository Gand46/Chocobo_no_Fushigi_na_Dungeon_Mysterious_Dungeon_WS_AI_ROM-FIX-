from pathlib import Path
from PIL import Image,ImageDraw
import struct,csv,sys
sys.path.insert(0,'delivery/Chocobo_EN_v1.1_HF11_TEST_Fuentes_QA16_M2_20261014/qa15')
from inventory_layout import story_inventory
R=Path('qa15/private/hf11_final/Chocobo_EN_v1.1_HF11_TEST.ws').read_bytes();J=Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws').read_bytes()
ids=[p.stem.replace('_',':') for p in sorted(Path('qa17/plans').glob('G*.lua'))]
for label,r in [('EN',R),('JP',J)]:
 rows,_=story_inventory(r,label);rows=[x for x in rows if x['id'] in ids];canvas=Image.new('RGB',(1200,2000),'white');d=ImageDraw.Draw(canvas);y=0
 for row in rows:
  a=int(row['pointer'],16);b=int(row['end'],16);words=list(struct.unpack('<'+'H'*((b-a)//2),r[a:b]));d.text((0,y),f"{row['id']} {a:06X}",fill='black');y+=15
  x=0
  for i,v in enumerate(words):
   if x>=1160:x=0;y+=43
   if 0<v<0x8000:
    off=0x160760+(v-1)*64;im=Image.new('RGB',(16,16),'white');p=im.load()
    for t in range(4):
     for yy in range(8):
      aa,bb=r[off+t*16+yy*2:off+t*16+yy*2+2]
      for xx in range(8):
       z=((aa>>(7-xx))&1)+2*((bb>>(7-xx))&1);c=[255,170,85,0][z];p[(t//2)*8+xx,(t%2)*8+yy]=(c,c,c)
    canvas.paste(im,(x,y))
   d.text((x,y+17),f'{i}:{v:04X}',fill='black');x+=52
  y+=47
 canvas.crop((0,0,1200,y)).save(f'qa17/streams_{label}.png')
