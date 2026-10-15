from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import random,json
r=Path('qa14');im=Image.open(r/'visual_A.png').convert('RGB');font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
bands=[[(34,65,76,96),(68,77,87,95),(83,73,101,93),(100,75,114,95),(113,72,130,93),(126,67,143,96),(141,75,155,95),(151,64,160,78),(155,70,190,96)],[(36,91,53,107),(52,92,65,108),(64,92,74,107),(73,89,82,107),(81,92,92,107),(91,91,99,107),(98,92,111,108),(113,90,128,107),(127,92,139,107),(138,92,150,107),(148,90,160,108),(158,92,171,107),(169,92,181,107),(179,92,190,107)],[(65,108,74,122),(72,108,81,122),(79,108,86,122),(87,108,99,122),(98,108,106,122),(105,108,113,122),(112,108,120,122),(119,108,127,122),(125,108,132,122),(131,108,140,122),(139,108,147,122),(146,108,153,122),(152,108,160,122)]]
entries=[{'band':b,'position':i,'box':box} for b,boxes in enumerate(bands) for i,box in enumerate(boxes)];random.Random(201410).shuffle(entries)
for i,x in enumerate(entries):x['id']=f'R{i+1:02d}'
(r/'refined_geometry_key.json').write_text(json.dumps(entries,indent=2)+'\n')
for page in range(2):
 group=entries[page*18:(page+1)*18];sheet=Image.new('RGB',(900,600),(238,238,232));d=ImageDraw.Draw(sheet)
 for i,item in enumerate(group):
  x=10+(i%6)*150;y=10+(i//6)*195;crop=im.crop(item['box']);d.text((x,y),item['id'],font=font,fill='black');sheet.paste(crop,(x+30,y+22));scale=min(4,130//crop.width);zoom=crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST);sheet.paste(zoom,(x+(135-zoom.width)//2,y+70))
 sheet.save(r/f'refined_page_{page+1}.png')
