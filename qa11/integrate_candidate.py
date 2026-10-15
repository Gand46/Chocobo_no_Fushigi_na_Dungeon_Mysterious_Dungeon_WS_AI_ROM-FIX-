from pathlib import Path
import struct,json,hashlib,sys
from PIL import Image
ROOT=Path('delivery/Chocobo_EN_v1.1_HF7_TEST_Fuentes_QA10_20261014');sys.path.insert(0,str(ROOT/'tools'))
from generate_whistle_fix import decode,encode
r=Path('private_roms/hf6_release/Chocobo_EN_v1.1_HF6_TEST.ws').read_bytes();assert hashlib.sha256(r).hexdigest()=='87ecaab08786651ee9431d6e386b0b73147e759aee282c053f6a75249e820d73'
frame=Image.open('qa11/Chocobo_WS_Logo_EN_v0.1/build/frames/frame_000.png');assert frame.mode=='P' and frame.size==(224,144)
pix=list(frame.getdata());assert set(pix)<=set(range(4));gfx=bytearray(r[0x155155:0x156b05]);maps=[]
for st in (0x150034,0x1501b7):maps.append(list(struct.unpack('<1024H',decode(r,st)[0])))
for y in range(7,16):
 for x in range(32):maps[0][y*32+x]=0x800;maps[1][y*32+x]=0x201
# Old Japanese lettering sprites only; native portrait animation is immutable.
gfx[392*16:411*16]=bytes(19*16)
free=list(range(0x3d,0xc3))+list(range(0xd7,0x148));lookup={};allocation=[]
for ty in range(7,16):
 for tx in range(28):
  tile=bytearray()
  for y in range(8):
   row=pix[(ty*8+y)*224+tx*8:(ty*8+y)*224+tx*8+8]
   # Only the provided static artwork; prompt remains the game's native sprite.
   if ty*8+y>=121:row=[3]*8
   for bit in range(2):tile.append(sum(((int(v)>>bit)&1)<<(7-x) for x,v in enumerate(row)))
  raw=bytes(tile)
  if raw==b'\xff'*16:idx=0xc3
  elif raw in lookup:idx=lookup[raw]
  else:
   assert free,'Native title tile budget exceeded'
   idx=free.pop(0);lookup[raw]=idx;gfx[idx*16:(idx+1)*16]=raw;allocation.append(idx)
  maps[1][ty*32+tx]=(idx-0xc2)+0x200
edits=[]
def edit(i,off,b):edits.append(dict(id=i,offset=hex(off),before=r[off:off+len(b)].hex(),after=b.hex(),reason='HF8: integrate user supplied English title pixels into native title resource; preserve native animation and prompt.'))
for i,(st,en) in enumerate([(0x150034,0x1501b7),(0x1501b7,0x1503c2)]):
 raw=struct.pack('<1024H',*[v&65535 for v in maps[i]]);c=encode(raw);assert decode(c,0)[0]==raw
 print('MAP',i,'compressed',len(c))
 if len(c)>en-st:
  assert i==1 and len(c)<=680
  edit('TITLE_MAP_PTR',0x150032,struct.pack('<H',0xfd58));st=0x15fd58;en=st+len(c);assert r[st:en]==b'\xff'*len(c)
 edit('TITLE_MAP_'+str(i),st,c+b'\xff'*(en-st-len(c)))
edit('TITLE_BITMAP_EN',0x155155,bytes(gfx))
assert gfx[328*16:392*16]==r[0x155155+328*16:0x155155+392*16]
b=bytearray(r)
for e in edits:off=int(e['offset'],0);a=bytes.fromhex(e['after']);assert b[off:off+len(a)]==bytes.fromhex(e['before']);b[off:off+len(a)]=a
b[0x16f1d4:0x16f1d6]=b'\xff\xff';b[-2:]=struct.pack('<H',sum(b[:-2])&65535)
Path('private_roms/qa11_title.ws').write_bytes(b)
Path('qa11/title_edits.json').write_text(json.dumps(edits,indent=2))
Path('qa11/integration.json').write_text(json.dumps({'asset_source':'Chocobo_WS_Logo_EN_v0.1','allocated_tiles':allocation,'new_tiles':len(allocation),'animation_unchanged':True,'rom_sha256':hashlib.sha256(b).hexdigest(),'artifact_method':'Native pattern and map replacement; no playback code modification; source rows56..120 and native animation overlay'},indent=2))
print('tiles',len(allocation),'sha',hashlib.sha256(b).hexdigest())
