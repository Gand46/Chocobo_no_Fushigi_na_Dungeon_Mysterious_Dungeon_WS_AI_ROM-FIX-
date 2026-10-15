from pathlib import Path
import struct,json,hashlib
BASE=Path('private_roms/hf2_build/Chocobo_EN_v1.1_HF2_TEST.ws')
EXPECTED='605ef4467766d778d74f01edee57ed1794698fd587056b2cff1f542e61b41864'
def decode(r,start):
 n=struct.unpack_from('<H',r,start)[0];p=start+2;b=bytearray()
 while len(b)<n:
  flags=r[p];p+=1
  for bit in range(8):
   if len(b)>=n:break
   if flags>>bit&1:b.append(r[p]);p+=1
   else:
    v=struct.unpack_from('<H',r,p)[0];p+=2;src=len(b)-(v>>4)
    for _ in range((v&15)+3):b.append(b[src] if src>=0 else 0);src+=1
 return bytes(b),p
def encode(b):
 out=bytearray(struct.pack('<H',len(b)));i=0
 while i<len(b):
  f=len(out);out.append(0)
  for bit in range(8):
   if i==len(b):break
   best=0;distance=0
   for d in range(1,min(i,4095)+1):
    n=0
    while n<18 and i+n<len(b) and b[i+n]==b[i+n-d]:n+=1
    if n>best:best=n;distance=d
    if best==18:break
   if best>=3:out.extend(struct.pack('<H',(distance<<4)|(best-3)));i+=best
   else:out[f]|=1<<bit;out.append(b[i]);i+=1
 return bytes(out)
def generate(r):
 assert hashlib.sha256(r).hexdigest()==EXPECTED
 gfx,end=decode(r,0x105b76);m,endm=decode(r,0x130c48)
 assert len(gfx)==37*16 and end==0x105cba and endm==0x130deb
 fixed=bytearray(m);counts={0:0,1:0,2:0}
 for i in range(0,len(m),2):
  w=struct.unpack_from('<H',m,i)[0]
  if w&511==37:
   pal=(w>>9)&15;assert pal in counts;counts[pal]+=1
   # Palette aliases of solid color 2 are equivalent to colors 1 and 3.
   # Baking aliases into tile pixels survives the native whole-map palette animation.
   w=(w&0xc000)+{0:37,1:38,2:39}[pal];struct.pack_into('<H',fixed,i,w)
 assert sum(counts.values())==18
 newgfx=gfx+bytes.fromhex('00ff')*8+bytes.fromhex('ff00')*8+bytes.fromhex('ffff')*8
 cg=encode(newgfx);cm=encode(fixed)
 assert decode(cg,0)[0]==newgfx and decode(cm,0)[0]==fixed
 edits=[]
 for ident,offset,after in [('WHISTLE_TILES_PTR',0x100078,struct.pack('<H',0xc800)),('WHISTLE_MAP_PTR',0x130040,struct.pack('<H',0xfc60)),('WHISTLE_COMPLETE_TILES',0x10c800,cg),('WHISTLE_NORMALIZED_MAP',0x13fc60,cm)]:
  before=r[offset:offset+len(after)]
  if len(after)>2:assert before==b'\xff'*len(after)
  edits.append(dict(id=ident,offset=hex(offset),before=before.hex(),after=after.hex(),reason='Complete the Whistle tile resource and bake solid-color palette aliases into valid tiles; same-bank resource relocation; original tiles 0..36 unchanged.'))
 assert 0xfc60+len(cm)<0x10000
 return edits,dict(original_tiles=37,new_tiles=40,changed_cells=18,palette_alias_counts=counts,compressed_tiles_bytes=len(cg),compressed_map_bytes=len(cm),unchanged_original_tiles=True)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description="Regenerate the four HF3 Whistle edits from the pinned HF2 image")
 p.add_argument('hf2_rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 edits,report=generate(a.hf2_rom.read_bytes());a.out.write_text(json.dumps(edits,indent=2)+'\n');print(json.dumps(report,indent=2))
