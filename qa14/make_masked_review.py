from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import random,json,hashlib
r=Path('qa14');im=Image.open(r/'visual_A.png').convert('RGB');font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
# Geometric crops only. No expected-character labels are supplied to recognition.
bands=[[(34,67,76,95),(68,72,87,96),(83,72,102,92),(100,75,115,94),(113,71,131,93),(125,68,143,96),(141,73,156,93),(153,65,161,76),(155,70,190,95)],[(36,92,53,106),(52,93,66,107),(65,93,75,106),(73,90,84,106),(82,93,92,106),(91,92,101,106),(100,93,113,107),(114,91,128,106),(127,94,139,106),(138,94,150,106),(149,91,161,108),(160,94,172,106),(170,94,181,106),(180,94,190,106)],[(65,109,73,121),(71,112,79,121),(77,113,85,121),(88,109,99,121),(98,113,106,121),(104,113,112,121),(111,109,120,121),(118,113,126,121),(124,113,132,121),(130,109,139,121),(138,113,147,121),(145,113,153,121),(151,113,159,121)]]
entries=[{'band':b,'position':i,'box':box} for b,boxes in enumerate(bands) for i,box in enumerate(boxes)];random.Random(41014).shuffle(entries)
for i,x in enumerate(entries):x['id']=f'G{i+1:02d}'
(r/'masked_geometry_key.json').write_text(json.dumps(entries,indent=2)+'\n')
for page in range(2):
 group=entries[page*18:(page+1)*18];sheet=Image.new('RGB',(900,600),(238,238,232));d=ImageDraw.Draw(sheet)
 for i,item in enumerate(group):
  x=10+(i%6)*150;y=10+(i//6)*195;crop=im.crop(item['box']);d.text((x,y),item['id'],font=font,fill='black')
  sheet.paste(crop,(x+30,y+22));scale=min(4,130//crop.width);zoom=crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST);sheet.paste(zoom,(x+(135-zoom.width)//2,y+70))
 sheet.save(r/f'masked_page_{page+1}.png')
