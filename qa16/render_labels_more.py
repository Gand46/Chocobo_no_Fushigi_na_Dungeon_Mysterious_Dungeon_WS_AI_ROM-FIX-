from pathlib import Path
from PIL import Image,ImageDraw
import csv,struct
r=Path('qa15/private/hf11_final/Chocobo_EN_v1.1_HF11_TEST.ws').read_bytes();base=Path('delivery/Chocobo_EN_v1.1_HF11_TEST_Fuentes_QA15_M1_20261014')
rows=list(csv.DictReader((base/'qa15/census_final/HF11_getter.csv').open()))
def glyph(v):
 im=Image.new('RGB',(16,16),'white');p=im.load();off=0x160760+(v-1)*64
 if v<=0 or v>=0xfff0 or v&0x8000:return im
 for tile in range(4):
  for y in range(8):
   a,b=r[off+tile*16+y*2:off+tile*16+y*2+2]
   for x in range(8):
    z=((a>>(7-x))&1)+2*((b>>(7-x))&1);c=[255,170,85,0][z];p[(tile//2)*8+x,(tile%2)*8+y]=(c,c,c)
 return im
for fam in [5,11,12,13,14,15,17,18]:
 rr=[x for x in rows if int(x['family'])==fam and x['nonempty']=='True'];out=Image.new('RGB',(740,((len(rr)+1)//2)*22),'white');d=ImageDraw.Draw(out)
 for i,x in enumerate(rr):
  xx=(i%2)*370;yy=(i//2)*22;d.text((xx,yy),x['id'],fill='black');pos=xx+78
  for off in range(int(x['pointer'],16),int(x['end'],16)-2,2):
   v=struct.unpack_from('<H',r,off)[0]
   if pos+16>xx+370:break
   out.paste(glyph(v),(pos,yy));pos+=16
 out.save(f'qa16/family{fam}.png')
