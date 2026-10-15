#!/usr/bin/env python3
"""Compile the supplied editable title assets into bounded native ROM edits.

Requires Pillow and NumPy only for asset regeneration. Ordinary build.py uses
these checked edits and has no third-party dependencies. Input is the original
Japanese ROM, never an already-patched ROM. No original game source is assumed.
"""
from pathlib import Path
import sys,struct,json,hashlib,subprocess,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
from build import replace_checked
from generate_whistle_fix import decode,encode
from PIL import Image

def generate(original,asset_root):
 manifest=json.loads((ROOT/'manifest.json').read_text())
 if hashlib.sha256(original).hexdigest()!=manifest['original']['sha256'] or len(original)!=manifest['original']['bytes']:
  raise ValueError('Incorrect Japanese base; see manifest.json')
 r=bytearray(original)
 replace_checked(r,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits'])
 corrections=json.loads((ROOT/'src/corrections.json').read_text())
 replace_checked(r,[e for e in corrections['edits'] if not e['id'].startswith('TITLE_')])
 # Rebuild directly from the native PNG sources, original GIF and composition rules.
 subprocess.run([sys.executable,str(asset_root/'tools/build.py')],cwd=asset_root,check=True,capture_output=True)
 frame=Image.open(asset_root/'build/frames/frame_000.png')
 if frame.mode!='P' or frame.size!=(224,144):raise ValueError('Expected indexed native 224x144 frame')
 pix=list(frame.getdata())
 if not set(pix)<=set(range(4)):raise ValueError('More than four palette indices')
 gfx=bytearray(r[0x155155:0x156b05]);maps=[]
 for st in (0x150034,0x1501b7):maps.append(list(struct.unpack('<1024H',decode(r,st)[0])))
 for y in range(7,16):
  for x in range(32):maps[0][y*32+x]=0x800;maps[1][y*32+x]=0x201
 gfx[392*16:411*16]=bytes(19*16)
 free=list(range(0x3d,0xc3))+list(range(0xd7,0x148));lookup={};allocation=[]
 for ty in range(7,16):
  for tx in range(28):
   tile=bytearray()
   for y in range(8):
    row=pix[(ty*8+y)*224+tx*8:(ty*8+y)*224+tx*8+8]
    if ty*8+y>=121:row=[3]*8
    for bit in range(2):tile.append(sum(((int(v)>>bit)&1)<<(7-x) for x,v in enumerate(row)))
   raw=bytes(tile)
   if raw==b'\xff'*16:idx=0xc3
   elif raw in lookup:idx=lookup[raw]
   else:
    if not free:raise ValueError('Native title tile budget exceeded')
    idx=free.pop(0);lookup[raw]=idx;gfx[idx*16:(idx+1)*16]=raw;allocation.append(idx)
   maps[1][ty*32+tx]=(idx-0xc2)+0x200
 edits=[]
 def edit(ident,off,b):edits.append(dict(id=ident,offset=hex(off),before=r[off:off+len(b)].hex(),after=b.hex(),reason='HF10: retain user supplied main title; compile native-grid subtitle for legibility; preserve animation and prompt.'))
 compressed=[]
 for n,(st,en) in enumerate([(0x150034,0x1501b7),(0x1501b7,0x1503c2)]):
  raw=struct.pack('<1024H',*[v&65535 for v in maps[n]]);packed=encode(raw)
  if decode(packed,0)[0]!=raw:raise ValueError('Map compression roundtrip failure')
  compressed.append(len(packed))
  if len(packed)>en-st:
   if n!=1 or len(packed)>680:raise ValueError('Same-bank map allocation exceeded')
   edit('TITLE_MAP_PTR',0x150032,struct.pack('<H',0xfd58));st=0x15fd58;en=st+len(packed)
   if r[st:en]!=b'\xff'*len(packed):raise ValueError('Title map cave is not free')
  edit('TITLE_MAP_'+str(n),st,packed+b'\xff'*(en-st-len(packed)))
 edit('TITLE_BITMAP_EN',0x155155,bytes(gfx))
 if gfx[328*16:392*16]!=r[0x155155+328*16:0x155155+392*16]:raise ValueError('Native animation changed')
 return edits,{'allocated_tiles':allocation,'tile_count':len(allocation),'tile_capacity':247,'compressed_map_bytes':compressed,'native_animation_tiles_328_391':'BYTE_IDENTICAL','source_static_rows':'56..120 inclusive','native_palette_rgb_at_steady_title':[[43,43,38],[152,149,139],[171,167,156],[224,219,205]],'font_system':'shared game font unchanged; supplied main artwork and HF10 title-specific subtitle font','asset_frame_sha256':hashlib.sha256((asset_root/'build/frames/frame_000.png').read_bytes()).hexdigest()}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('japanese_rom',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--report',type=Path);p.add_argument('--write-source',action='store_true',help='Replace only TITLE_ edits in src/corrections.json after successful generation');a=p.parse_args()
 edits,report=generate(a.japanese_rom.read_bytes(),ROOT/'assets/title/user_v02_subtitle');a.out.write_text(json.dumps(edits,indent=2)+'\n')
 if a.report:a.report.write_text(json.dumps(report,indent=2)+'\n')
 if a.write_source:
  dest=ROOT/'src/corrections.json';c=json.loads(dest.read_text());c['edits']=[e for e in c['edits'] if not e['id'].startswith('TITLE_')]+edits;dest.write_text(json.dumps(c,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
