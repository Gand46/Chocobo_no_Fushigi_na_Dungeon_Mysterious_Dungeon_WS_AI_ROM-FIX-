"""Export the runtime-linked native title tiles; does not translate the title."""
from pathlib import Path
import argparse,hashlib,json
from PIL import Image
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('rom',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
b=a.rom.read_bytes();raw=b[0x155155:0x156b05]
assert hashlib.sha256(raw).hexdigest()=='096b555e78fc03cf59a0fdaf91ec5ea577bf7d58dc88b36f1d08486223942b96','Unexpected asset preimage'
a.out.mkdir(parents=True,exist_ok=True)
(a.out/'title_native_2bpp.bin').write_bytes(raw)
im=Image.new('L',(16*8,26*8),255)
for t in range(411):
 for y in range(8):
  p0,p1=raw[t*16+y*2:t*16+y*2+2]
  for x in range(8):
   v=((p0>>(7-x))&1)|(((p1>>(7-x))&1)<<1)
   im.putpixel(((t%16)*8+x,(t//16)*8+y),255-v*85)
im.save(a.out/'title_tiles.png')
(a.out/'manifest.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(b).hexdigest(),'rom_range':'155155..156B04','bytes':len(raw),'tiles':411,'format':'planar2bpp16bytes/tile','consumer':'154A27..154A43 -> WRAM2000','asset_sha256':hashlib.sha256(raw).hexdigest(),'status':'EXTRACTED_UNTRANSLATED'},indent=2))
