"""Recreate the context-masked subtitle sheet, without expected-letter labels."""
from pathlib import Path
import json, random
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
out=Path(__file__).resolve().parent
image=Image.open(ROOT/'evidence/qa14_runs/title_portable/anim01000.png').convert('RGB')
layout=json.loads((ROOT/'assets/title/user_v02_subtitle/build/subtitle_layout_v02.json').read_text())
entries=[]
for glyph in layout['glyphs']:
    if glyph['character']==' ': continue
    a,b,c,d=glyph['ink_box']
    entries.append({'source_position':glyph['position'],'box':[65+a-1,109+b-1,65+c+1,109+d+1]})
random.Random(14102026).shuffle(entries)
canvas=Image.new('RGB',(780,390),(238,238,232)); draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for i,entry in enumerate(entries):
    entry['id']=f'P{i+1:02d}'
    x=10+(i%7)*110; y=8+(i//7)*190
    crop=image.crop(entry['box'])
    draw.text((x,y),entry['id'],font=font,fill='black')
    canvas.paste(crop,(x+40,y+32))
    canvas.paste(crop.resize((crop.width*6,crop.height*6),Image.Resampling.NEAREST),(x+20,y+70))
canvas.save(out/'hf10_subtitle_masked.png')
(out/'hf10_subtitle_geometry.json').write_text(json.dumps(entries,indent=2)+'\n')
