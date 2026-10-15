from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qa15.inventory_layout import story_inventory,words_until_end
from qa22.hf16_base import input_path,reconstruct
J=input_path().read_bytes();E=reconstruct(J)
ids=json.loads(Path('qa22/audit_ids.json').read_text())
maps=[{x['id']:x for x in story_inventory(r,'x')[0]} for r in (J,E)]
def tile(r,v):
 im=Image.new('RGB',(16,16),'white');p=im.load()
 if not 0<v<0x1000:return im
 off=0x160760+(v-1)*64
 for t in range(4):
  for y in range(8):
   a,b=r[off+t*16+y*2:off+t*16+y*2+2]
   for x in range(8):
    z=((a>>(7-x))&1)+2*((b>>(7-x))&1);c=[255,170,85,0][z];p[t//2*8+x,t%2*8+y]=(c,c,c)
 return im
for start in range(0,len(ids),6):
 canvas=Image.new('RGB',(1500,10000),'#f0f0f0');d=ImageDraw.Draw(canvas);y=0
 for id in ids[start:start+6]:
  d.text((4,y),id,fill='black');y+=17;hs=[]
  for k,r in enumerate((J,E)):
   w,_,_=words_until_end(r,int(maps[k][id]['pointer'],16));x=k*750;top=y;col=0;row=0;i=0
   while i<len(w):
    v=w[i];i+=1
    if v>=0xfff0:
     token=f'<{v:04X}>'
     if v in (0xfff4,0xfff8,0xfffa,0xfffb):token+=f'{w[i]:04X}';i+=1
     d.text((x+col*32,top+row*46+31),token,fill='#ad2020')
     if v in (0xfff2,0xfffc,0xfffd,0xfffe):row+=1;col=0
     continue
    if col>=22:row+=1;col=0
    canvas.paste(tile(r,v).resize((32,32),Image.Resampling.NEAREST),(x+col*32,top+row*46));col+=1
   hs.append((row+1)*46)
  y+=max(hs)+15
 canvas.crop((0,0,1500,y)).save(f'qa22/audit_{start//6:02d}.png')
print('sheets',(len(ids)+5)//6)
