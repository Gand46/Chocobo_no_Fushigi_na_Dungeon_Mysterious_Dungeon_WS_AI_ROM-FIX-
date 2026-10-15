from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,struct,json
r=Path('runs');base=r/'q4_whistle_hf2_validation';fix=r/'q4_whistle_hf3_validation'
w=(base/'wram_animation.bin').read_bytes();nw=(fix/'wram_animation.bin').read_bytes();cells=[];mask=np.zeros((157,224),bool)
for a in range(0x1800,0x2000,2):
 v=struct.unpack_from('<H',w,a)[0]
 if v&511==0x1a5:
  y=(a-0x1800)//64*8;x=(((a-0x1800)%64)//2*8-240)%256;cells.append(a)
  if x<224 and y<144:mask[y:y+8,x:x+8]=True
allowed=set()
for a in cells:allowed.update([a,a+1])
mapdiff=[i for i in range(0x1800,0x2000)if w[i]!=nw[i]]
assert set(mapdiff)<=allowed
assert w[0x3800:0x3a50]==nw[0x3800:0x3a50]
assert nw[0x3a50:0x3a80]==bytes.fromhex('00ff')*8+bytes.fromhex('ff00')*8+bytes.fromhex('ffff')*8
rows=[]
for f in range(2,2401):
 a=np.array(Image.open(base/f'f{f:05}.png'));b=np.array(Image.open(fix/f'f{f:05}.png'));d=np.any(a!=b,axis=2)
 if d.any():
  ys,xs=np.where(d);rows.append(dict(frame=f,pixels=int(d.sum()),outside_repaired_cells=int((d&~mask).sum()),bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]))
out={'frames':2399,'excluded_first_frame':'emulator returned invalid PNG before first render','identical_frames':2399-len(rows),'different_frames':len(rows),'frames_with_changes_outside_repaired_cells':[x for x in rows if x['outside_repaired_cells']], 'all_differences':rows,'original_37_tiles_identical':True,'new_three_solid_tiles_verified':True,'changed_map_bytes_restricted_to_18_cells':True,'map_cells':[hex(a)for a in cells]}
Path('qa4/whistle_comparison.json').write_text(json.dumps(out,indent=2))
print({k:v for k,v in out.items()if k not in ('all_differences','frames_with_changes_outside_repaired_cells')});print('outside',out['frames_with_changes_outside_repaired_cells'][:20], 'count',len(out['frames_with_changes_outside_repaired_cells']))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
canvas=Image.new('RGB',(924,584),'#f0eee6');d=ImageDraw.Draw(canvas)
for i,f in enumerate([650,720,780]):
 for j,(folder,label) in enumerate([(base,'HF2: tile residual'),(fix,'HF3: recurso corregido')]):
  im=Image.open(folder/f'f{f:05}.png').resize((448,314),Image.Resampling.NEAREST)
  # Main pair plus small animation samples below.
  if i==1:canvas.paste(im,(8+j*460,40));d.text((8+j*460,12),label,font=font,fill='black')
  elif i==0:canvas.paste(Image.open(folder/f'f{f:05}.png'),(8+j*460,394))
  else:canvas.paste(Image.open(folder/f'f{f:05}.png'),(238+j*460,394))
d.text((8,363),'Secuencia real en Mesen: fotogramas 650, 720 y 780.',font=font,fill='black')
d.text((8,558),'HF3 TEST · inventario sintetico · tipografia original conservada',font=font,fill='black')
canvas.save('delivery/Chocobo_HF3_Silbato_20261013.png')
