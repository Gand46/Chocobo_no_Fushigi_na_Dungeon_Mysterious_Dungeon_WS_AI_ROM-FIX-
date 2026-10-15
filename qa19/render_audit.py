from pathlib import Path
from PIL import Image,ImageDraw
import sys,struct,json
sys.path.insert(0,'delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014/qa15');from inventory_layout import story_inventory,words_until_end
E=Path('qa18/private/hf13_release/Chocobo_EN_v1.1_HF13_TEST.ws').read_bytes();J=Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws').read_bytes();maps=[]
for r in [J,E]:rows,_=story_inventory(r,'x');maps.append({x['id']:x for x in rows})
ids=[x for x in maps[1]if x.startswith('G16:')and maps[1][x]['max_literal_cells']]+['G06:M073','G06:M099']
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
for start in range(0,len(ids),10):
 canvas=Image.new('RGB',(1500,3000),'#f0f0f0');d=ImageDraw.Draw(canvas);y=0
 for id in ids[start:start+10]:
  d.text((4,y),id,fill='black');y+=17;hs=[]
  for k,r in enumerate([J,E]):
   w,end,_=words_until_end(r,int(maps[k][id]['pointer'],16));x=k*750;top=y;col=0;row=0;i=0
   while i<len(w):
    v=w[i];i+=1
    if v>=0xfff0:
     token=f'<{v:04X}>'
     if v in [0xfff4,0xfff8,0xfffa,0xfffb]:token+=f'{w[i]:04X}';i+=1
     d.text((x+col*32,top+row*46+31),token,fill='#ad2020')
     if v in [0xfff2,0xfffc,0xfffd,0xfffe]:row+=1;col=0
     continue
    if col>=22:row+=1;col=0
    canvas.paste(tile(r,v).resize((32,32),Image.Resampling.NEAREST),(x+col*32,top+row*46));col+=1
   hs.append((row+1)*46)
  y+=max(hs)+15
 canvas.crop((0,0,1500,y)).save(f'qa19/audit_{start//10:02d}.png')
Path('qa19/audit_ids.json').write_text(json.dumps(ids,indent=2))
# Font atlas for reviewed encoder entries, not OCR.
for start in range(0,1024,128):
 can=Image.new('RGB',(16*64,8*55),'white');d=ImageDraw.Draw(can)
 for j in range(128):
  v=start+j;x=j%16*64;y=j//16*55;can.paste(tile(E,v).resize((32,32),Image.Resampling.NEAREST),(x,y));d.text((x,y+34),f'{v:04X}',fill='black')
 can.save(f'qa19/font_{start:03x}.png')
