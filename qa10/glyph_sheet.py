"""Arrange actual title glyph crops with neutral numeric labels for blind review."""
from PIL import Image,ImageDraw
from pathlib import Path
import random,json,sys
im=Image.open(sys.argv[1]);src=json.loads(Path(sys.argv[2]).read_text());g=src['glyphs'];parts=[]
for li,((sx,sy,gap),lay) in enumerate(zip([(3,3,4),(2,2,3),(1,1,3)],src['layout'])):
 x=lay['x'];y=lay['y']
 for c in lay['text']:
  wid=len(g[c][0])*sx
  if c!=' ':parts.append((c,li,im.crop((x-1,y-1,x+wid+3,min(144,y+7*sy+3)))))
  x+=wid+gap
random.Random(1467).shuffle(parts)
out=Image.new('RGB',(400,55*((len(parts)+9)//10)),(224,219,205));d=ImageDraw.Draw(out);answer={}
for i,(c,li,crop) in enumerate(parts):
 x=i%10*40;y=i//10*55;out.paste(crop,(x+3,y+15));d.text((x+4,y),str(i+1),fill=(43,43,38));answer[str(i+1)]={'glyph':c,'family':li}
out.save(sys.argv[3]);Path(sys.argv[3]+'.key.json').write_text(json.dumps(answer,indent=2))
