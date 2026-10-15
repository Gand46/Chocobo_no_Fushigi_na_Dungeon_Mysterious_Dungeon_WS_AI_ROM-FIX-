from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import random,json
r=Path('qa14');im=Image.open(r/'visual_A.png').convert('RGB');font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
bands=[[(34,65,76,96),(66,72,87,96),(83,73,101,93),(100,75,114,95),(113,72,130,93),(126,67,143,96),(141,75,155,95),(151,62,160,80),(155,70,190,96)],[(36,91,53,107),(52,92,65,108),(64,92,74,107),(73,89,82,107),(81,92,92,107),(91,91,99,107),(98,92,111,108),(113,90,128,107),(128,92,138,107),(138,92,148,107),(148,90,160,108),(158,92,168,107),(168,92,177,107),(177,92,189,107)],[(65, 108, 74, 122), (73, 108, 80, 122), (79, 108, 85, 122), (87, 108, 100, 122), (99, 108, 105, 122), (105, 108, 112, 122), (112, 108, 119, 122), (118, 108, 125, 122), (124, 108, 130, 122), (129, 108, 137, 122), (136, 108, 144, 122), (143, 108, 150, 122), (149, 108, 157, 122)]]
entries=[{'band':b,'position':i,'box':box} for b,boxes in enumerate(bands) for i,box in enumerate(boxes)];random.Random(201411).shuffle(entries)
for i,x in enumerate(entries):x['id']=f'V{i+1:02d}'
(r/'final_geometry_key.json').write_text(json.dumps(entries,indent=2)+'\n')
for page in range(2):
 group=entries[page*18:(page+1)*18];sheet=Image.new('RGB',(900,600),(238,238,232));d=ImageDraw.Draw(sheet)
 for i,item in enumerate(group):
  x=10+(i%6)*150;y=10+(i//6)*195;crop=im.crop(item['box']);d.text((x,y),item['id'],font=font,fill='black');sheet.paste(crop,(x+30,y+22));scale=min(4,130//crop.width);zoom=crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST);sheet.paste(zoom,(x+(135-zoom.width)//2,y+70))
 sheet.save(r/f'final_page_{page+1}.png')
