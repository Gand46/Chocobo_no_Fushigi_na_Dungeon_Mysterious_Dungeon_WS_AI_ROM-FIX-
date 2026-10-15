from PIL import Image,ImageDraw
from pathlib import Path
import sys
p=Path(sys.argv[1]);fs=sorted(p.glob('f*.png'))[::int(sys.argv[2]) if len(sys.argv)>2 else 1]
o=Image.new('RGB',(224*5,166*((len(fs)+4)//5)),'white');d=ImageDraw.Draw(o)
for i,f in enumerate(fs):
 x=i%5*224;y=i//5*166;o.paste(Image.open(f),(x,y+20));d.text((x,y),f.stem,fill='black')
o.save(p/'sheet.png')
