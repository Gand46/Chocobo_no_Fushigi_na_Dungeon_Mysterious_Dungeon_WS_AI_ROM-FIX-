"""Historical HF7 lettering generator. HF8 uses integrate_title_assets.py and assets/title/user_v01."""
"""Editable, bounded native 2bpp title localization; no shared font modification."""
from pathlib import Path
import sys, struct, json, hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from generate_whistle_fix import decode,encode

# Canonical pixel stencils. Outlined/slanted large letters extend the native
# title's angular strokes, light face, dark outline and offset lower shadow.
GLYPHS={
'A':['00100','01110','11011','11011','11111','11011','11011'],
'B':['11110','11011','11011','11110','11011','11011','11110'],
'C':['01111','11000','11000','11000','11000','11000','01111'],
'D':['11110','11011','11011','11011','11011','11011','11110'],
'E':['11111','11000','11000','11110','11000','11000','11111'],
'F':['11111','11000','11000','11110','11000','11000','11000'],
'G':['01111','11000','11000','11011','11011','11011','01110'],
'H':['11011','11011','11011','11111','11011','11011','11011'],
'I':['111','010','010','010','010','010','111'],
'M':['1100011','1110111','1111111','1101011','1100011','1100011','1100011'],
'N':['1100011','1110011','1111011','1101111','1100111','1100011','1100011'],
'O':['01110','11011','11011','11011','11011','11011','01110'],
'R':['11110','11011','11011','11110','11100','11010','11011'],
'S':['01111','11000','11000','01110','00011','00011','11110'],
'T':['11111','00100','00100','00100','00100','00100','00100'],
'U':['11011','11011','11011','11011','11011','11011','01110'],
'W':['1100011','1100011','1100011','1101011','1111111','1110111','1100011'],
'Y':['11011','11011','01110','00100','00100','00100','00100'],
"'":['11','11','10','00','00','00','00'],
' ':['000']*7}

def packtile(p):
 b=bytearray()
 for row in p:
  b.extend([sum((v&1)<<(7-x) for x,v in enumerate(row)),sum(((v>>1)&1)<<(7-x) for x,v in enumerate(row))])
 return bytes(b)

def generate(r):
 assert hashlib.sha256(r).hexdigest()=='87ecaab08786651ee9431d6e386b0b73147e759aee282c053f6a75249e820d73'
 gfx=bytearray(r[0x155155:0x156b05]);maps=[]
 for start in [0x150034,0x1501b7]:
  raw,end=decode(r,start);maps.append(list(struct.unpack('<1024H',raw)))
 # Keep the upper crystal and animated Chocobo. Remove the old lettering,
 # including sprite lettering 392..410, while keeping animation tiles328..391.
 for y in range(7,15):
  for x in range(32):maps[0][y*32+x]=0x800;maps[1][y*32+x]=0x201
 gfx[392*16:411*16]=bytes(19*16)
 canvas=[[3]*224 for _ in range(64)]
 def lettering(text,y,sx,sy,slant=False):
  gap=4 if slant else 3
  width=sum(len(GLYPHS[c][0])*sx+gap for c in text)-gap
  x0=(224-width)//2;mask=set();xx=x0
  for ch in text:
   for gy,row in enumerate(GLYPHS[ch]):
    for gx,v in enumerate(row):
     if v=='1':
      for dy in range(sy):
       for dx in range(sx):mask.add((xx+gx*sx+dx+((6-gy)//6 if slant else 0),y+gy*sy+dy))
   xx+=len(GLYPHS[ch][0])*sx+gap
  if sy==1:
   for x,yy in mask:canvas[yy][x]=1
   return {'text':text,'x':x0,'y':y+56,'width':width,'height':7}
  for dx,dy in [(2,2),(1,2),(2,1),(0,-1),(-1,0),(1,0),(0,1),(-1,-1),(1,1)]:
   for x,yy in mask:
    if 0<=x+dx<224 and 0<=yy+dy<64:canvas[yy+dy][x+dx]=0
  for x,yy in mask:canvas[yy][x]=3 if (yy-y)<sy*4 else 2
  return {'text':text,'x':x0,'y':y+56,'width':width+4,'height':7*sy+4}
 layout=[lettering("CHOCOBO'S",9,3,3,True),lettering('MYSTERY DUNGEON',34,2,2),lettering('FOR WONDERSWAN',55,1,1)]
 # Reuse only tiles formerly occupied by title text, never the animation.
 free=list(range(0x3d,0xc3))+list(range(0xd7,0x148));used={};allocation=[]
 for y in range(8):
  for x in range(28):
   t=packtile([row[x*8:x*8+8] for row in canvas[y*8:y*8+8]])
   if t==b'\xff'*16:idx=0xc3
   elif t in used:idx=used[t]
   else:
    idx=free.pop(0);used[t]=idx;gfx[idx*16:(idx+1)*16]=t;allocation.append(idx)
   maps[1][(y+7)*32+x]=(idx-0xc2)+0x200
 # Index words are stored relative to their descriptor's tile base.
 edits=[]
 def edit(ident,off,b,reason):
  edits.append(dict(id=ident,offset=hex(off),before=r[off:off+len(b)].hex(),after=b.hex(),reason=reason))
 for n,(st,en) in enumerate([(0x150034,0x1501b7),(0x1501b7,0x1503c2)]):
  raw=struct.pack('<1024H',*[v&65535 for v in maps[n]]);comp=encode(raw);assert decode(comp,0)[0]==raw
  if len(comp)>en-st:
   assert n==1 and len(comp)<=0x10000-0xfd58,(n,len(comp))
   edit('TITLE_MAP_PTR',0x150032,struct.pack('<H',0xfd58),'Same-bank relocation of map1; old compressed map retained.')
   st=0x15fd58;en=st+len(comp);assert r[st:en]==b'\xff'*len(comp)
  edit('TITLE_MAP_'+str(n),st,comp+b'\xff'*(en-st-len(comp)),'Native map format and descriptor unchanged; remove Japanese title and map English title tiles.')
 edit('TITLE_BITMAP_EN',0x155155,bytes(gfx),'Native 411-tile 2bpp title resource; Chocobo animation328..391 and upper crystal retained. Only title artwork changes.')
 return edits,{'layout':layout,'allocated_tiles':allocation,'animation_unchanged':gfx[328*16:392*16]==r[0x155155+328*16:0x155155+392*16],'title_sha256':hashlib.sha256(gfx).hexdigest(),'glyphs':GLYPHS}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('hf6_rom',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--source-out',type=Path)
 a=p.parse_args();edits,report=generate(a.hf6_rom.read_bytes());a.out.write_text(json.dumps(edits,indent=2)+'\n')
 if a.source_out:a.source_out.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ['glyphs','allocated_tiles']},indent=2))
